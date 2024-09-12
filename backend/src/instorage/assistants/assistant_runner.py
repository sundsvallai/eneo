from typing import Optional

from instorage.ai_models.ai_models_service import AIModelsService
from instorage.ai_models.completion_models.completion_service import (
    CompletionService,
    count_tokens,
)
from instorage.ai_models.embedding_models.datastore.datastore import Datastore
from instorage.assistants.api.assistant_models import AssistantResponse
from instorage.assistants.assistant import Assistant
from instorage.files.file_models import FileType
from instorage.files.file_service import FileService
from instorage.groups.group import GroupInDB
from instorage.info_blobs.info_blob import InfoBlobChunkInDBWithScore, InfoBlobInDB
from instorage.info_blobs.info_blob_repo import InfoBlobRepository
from instorage.main.exceptions import BadRequestException
from instorage.main.logging import get_logger
from instorage.main.models import ModelId
from instorage.services.service import DatastoreResult
from instorage.sessions.session import SessionInDB
from instorage.sessions.session_service import SessionService
from instorage.spaces.space_service import SpaceService
from instorage.websites.website_models import Website

logger = get_logger(__name__)


class RunnerDelegate:
    def __init__(
        self,
        info_blobs_repo: InfoBlobRepository,
        datastore: Datastore,
    ):
        self.info_blobs_repo = info_blobs_repo
        self.datastore = datastore

    async def _query_datastore_if_groups_or_websites(
        self,
        input_string: str,
        groups: list[GroupInDB],
        websites: list[Website],
    ):
        if (groups or websites) and input_string:
            info_blob_chunks = await self.datastore.semantic_search(
                input_string, groups, websites, autocut_cutoff=3
            )

            return info_blob_chunks

        return []

    async def _get_info_blobs_from_chunks(
        self, info_blob_chunks: list[InfoBlobChunkInDBWithScore]
    ):
        info_blobs = []
        for chunk in info_blob_chunks:
            info_blob = await self.info_blobs_repo.get(chunk.info_blob_id)

            info_blobs.append(info_blob)

        return info_blobs

    def _get_info_blob_chunks_without_duplicates(
        self, info_blob_chunks: list[InfoBlobChunkInDBWithScore]
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
        info_blob_chunks: list[InfoBlobChunkInDBWithScore],
        info_blobs: list[InfoBlobInDB],
    ):
        info_blob_ids = {blob.id for blob in info_blobs}
        return [
            chunk for chunk in info_blob_chunks if chunk.info_blob_id in info_blob_ids
        ]

    async def get_references(
        self,
        input_string: str,
        groups: list[GroupInDB],
        websites: list[Website] = [],
    ):
        chunks = await self._query_datastore_if_groups_or_websites(
            input_string, groups, websites
        )
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
        assistant: Assistant,
        session_service: SessionService,
        completion_service: CompletionService,
        file_service: FileService,
        runner_delegate: RunnerDelegate,
        ai_models_service: AIModelsService,
        space_service: SpaceService,
    ):
        self.assistant = assistant
        self.session_service = session_service
        self.completion_service = completion_service
        self.file_service = file_service
        self.delegate = runner_delegate
        self.ai_models_service = ai_models_service
        self.space_service = space_service

    async def _check_assistant_models(self):
        if self.assistant.completion_model.id is not None:
            completion_model = await self.ai_models_service.get_completion_model(
                self.assistant.completion_model.id
            )

        if self.assistant.space_id is not None:
            space = await self.space_service.get_space(self.assistant.space_id)

            if (
                self.assistant.completion_model.id
                and not space.is_completion_model_in_space(
                    self.assistant.completion_model.id
                )
            ):
                raise BadRequestException(
                    f"Completion Model {completion_model.name} is not in space."
                )

            for item in self.assistant.groups + self.assistant.websites:
                if not space.is_embedding_model_in_space(item.embedding_model.id):
                    raise BadRequestException(
                        f"Embedding Model {item.embedding_model.name} is not in space."
                    )

    async def run(
        self,
        question: str,
        file_ids: list[ModelId] = [],
        session: SessionInDB | None = None,
        stream: bool = True,
        datastore_result: DatastoreResult | None = None,
    ) -> AssistantResponse:
        await self._check_assistant_models()

        files = await self.file_service.get_files_by_ids(file_ids)

        if datastore_result is None:
            # Embed the whole conversation
            if files:
                files_text = "\n".join(
                    file.text for file in files if file.file_type == FileType.TEXT
                )
                search_query = f"{files_text}\n{question}"
            else:
                search_query = question

            concatenated_convo = self.delegate.concatenate_conversation(
                session=session,
                question=search_query,
            )
            datastore_result = await self.delegate.get_references(
                input_string=concatenated_convo,
                groups=self.assistant.groups,
                websites=self.assistant.websites,
            )

        ai_response = await self.completion_service.get_response(
            question=question,
            files=files,
            prompt=self.assistant.prompt,
            info_blob_chunks=datastore_result.chunks,
            session=session,
            stream=stream,
            extended_logging=self.assistant.logging_enabled,
            model_kwargs=self.assistant.completion_model_kwargs,
        )

        if session is None:
            # Set name of session to question or files names
            name = question
            if not name and files:
                name = " ".join(file.name for file in files)

            session = await self.session_service.create_session(
                name=name, assistant=self.assistant
            )

        if stream:

            async def response_stream():
                response = []

                async for chunk in ai_response.completion:
                    yield chunk
                    response.append(chunk)

                response_string = "".join(response)
                total_response_tokens = count_tokens(response_string)
                await self.session_service.add_question_to_session(
                    question=question,
                    answer=response_string,
                    num_tokens_question=ai_response.total_token_count,
                    num_tokens_answer=total_response_tokens,
                    files=files,
                    completion_model=self.assistant.completion_model,
                    info_blob_chunks=datastore_result.no_duplicate_chunks,
                    session=session,
                    logging_details=ai_response.extended_logging,
                )

            answer = response_stream()

        else:
            answer = ai_response.completion
            total_response_tokens = count_tokens(answer)
            await self.session_service.add_question_to_session(
                question=question,
                answer=answer,
                num_tokens_question=ai_response.total_token_count,
                num_tokens_answer=total_response_tokens,
                files=files,
                completion_model=self.assistant.completion_model,
                info_blob_chunks=datastore_result.no_duplicate_chunks,
                session=session,
                logging_details=ai_response.extended_logging,
            )

        response = AssistantResponse(
            question=question,
            files=files,
            session=session,
            answer=answer,
            info_blobs=datastore_result.info_blobs,
            completion_model=self.assistant.completion_model,
        )

        return response
