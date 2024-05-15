from typing import Optional

from instorage.ai_models.completion_models.completion_model_service import (
    CompletionModelService,
)
from instorage.ai_models.completion_models.llms import CompletionModel
from instorage.ai_models.embedding_models.datastore.datastore import Datastore
from instorage.assistants.assistant import AssistantInDBWithUser, AssistantResponse
from instorage.groups.group import GroupInDB
from instorage.info_blobs.info_blob import InfoBlobChunkWithScore, InfoBlobInDB
from instorage.info_blobs.info_blob_repo import InfoBlobRepository
from instorage.main.logging import get_logger
from instorage.services.service import DatastoreResult
from instorage.sessions.session import SessionInDB
from instorage.sessions.session_service import SessionService

logger = get_logger(__name__)


class RunnerDelegate:
    def __init__(
        self,
        info_blobs_repo: InfoBlobRepository,
        datastore: Datastore,
        groups: list[GroupInDB],
    ):
        self.info_blobs_repo = info_blobs_repo
        self.datastore = datastore
        self.groups = groups

    async def _query_datastore_if_groups(self, input_string: str):
        if self.groups:
            info_blob_chunks = await self.datastore.semantic_search(
                input_string, self.groups
            )

            return info_blob_chunks

        return []

    async def _get_info_blobs_from_chunks(
        self, info_blob_chunks: list[InfoBlobChunkWithScore]
    ):
        info_blobs = []
        for chunk in info_blob_chunks:
            info_blob = await self.info_blobs_repo.get_by_uuid(chunk.info_blob_id)

            info_blobs.append(info_blob)

        return info_blobs

    def _get_info_blob_chunks_without_duplicates(
        self, info_blob_chunks: list[InfoBlobChunkWithScore]
    ):
        c = {}

        for chunk in info_blob_chunks:
            if (
                c.get(chunk.info_blob_id) is None
                or c[chunk.info_blob_id].score < chunk.score
            ):
                c[chunk.info_blob_id] = chunk

        return list(c.values())

    def _remove_chunks_without_info_blob(
        self,
        info_blob_chunks: list[InfoBlobChunkWithScore],
        info_blobs: list[InfoBlobInDB],
    ):
        info_blob_ids = {blob.id for blob in info_blobs}
        return [
            chunk for chunk in info_blob_chunks if chunk.info_blob_id in info_blob_ids
        ]

    async def get_references(self, input_string: str):
        chunks = await self._query_datastore_if_groups(input_string)
        no_duplicate_chunks = self._get_info_blob_chunks_without_duplicates(chunks)
        info_blobs = await self._get_info_blobs_from_chunks(no_duplicate_chunks)

        return DatastoreResult(
            chunks=chunks,
            no_duplicate_chunks=no_duplicate_chunks,
            info_blobs=info_blobs,
        )

    def concatenate_conversation(self, session: Optional[SessionInDB], question: str):
        if session is None:
            return question

        conversation_string = (
            "\n".join(
                "\n".join((question.question, question.answer))
                for question in session.questions
            )
            + f"\n{question}"
        )

        return conversation_string.strip()


class AssistantRunner:
    def __init__(
        self,
        assistant: AssistantInDBWithUser,
        session_service: SessionService,
        completion_model_service: CompletionModelService,
        runner_delegate: RunnerDelegate,
        completion_model: CompletionModel,
    ):
        self.assistant = assistant
        self.session_service = session_service
        self.completion_model_service = completion_model_service
        self.delegate = runner_delegate
        self.completion_model = completion_model

    async def run(
        self,
        question: str,
        session: SessionInDB = None,
        stream: bool = True,
        datastore_result: DatastoreResult = None,
    ) -> AssistantResponse:
        if datastore_result is None:
            # Embed the whole conversation
            concatenated_convo = self.delegate.concatenate_conversation(
                session, question
            )
            datastore_result = await self.delegate.get_references(concatenated_convo)

        ai_response = await self.completion_model_service.get_response(
            question=question,
            prompt=self.assistant.prompt,
            info_blobs=datastore_result.chunks,
            session=session,
            stream=stream,
            extended_logging=self.assistant.logging_enabled,
        )

        if session is None:
            # Set name of session to question
            session = await self.session_service.create_session(
                name=question, assistant=self.assistant
            )

        if stream:

            async def response_stream():
                response = []
                async for chunk in ai_response.completion:
                    yield chunk
                    response.append(chunk)

                response_string = "".join(response)
                await self.session_service.add_question_to_session(
                    question=question,
                    answer=response_string,
                    model=ai_response.model,
                    info_blob_chunks=datastore_result.no_duplicate_chunks,
                    session=session,
                    logging_details=ai_response.extended_logging,
                )

            answer = response_stream()

        else:
            answer = ai_response.completion
            await self.session_service.add_question_to_session(
                question=question,
                answer=answer,
                model=ai_response.model,
                info_blob_chunks=datastore_result.no_duplicate_chunks,
                session=session,
                logging_details=ai_response.extended_logging,
            )

        response = AssistantResponse(
            session=session,
            answer=answer,
            info_blobs=datastore_result.info_blobs,
            model=self.completion_model,
        )

        return response
