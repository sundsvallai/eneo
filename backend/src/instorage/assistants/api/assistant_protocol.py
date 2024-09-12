from typing import Optional

from sse_starlette import EventSourceResponse

from instorage.ai_models.completion_models.completion_model import CompletionModel
from instorage.assistants.api.assistant_models import AskAssistant
from instorage.database.database import AsyncSession
from instorage.database.transaction import gen_transaction
from instorage.files.file_models import File, FilePublic
from instorage.info_blobs.info_blob import (
    InfoBlobInDB,
    InfoBlobMetadata,
    InfoBlobPublicNoText,
)
from instorage.main.logging import get_logger
from instorage.sessions.session import AskResponse, SessionInDB
from instorage.workflows.assistant_guard_runner import AssistantGuardRunner

logger = get_logger(__name__)


def to_ask_reponse(
    question: str,
    files: list[File],
    session: SessionInDB,
    answer: str,
    info_blobs: list[InfoBlobInDB],
    completion_model: Optional[CompletionModel] = None,
):
    return AskResponse(
        question=question,
        files=[FilePublic(**file.model_dump()) for file in files],
        session_id=session.id,
        answer=answer,
        references=[
            InfoBlobPublicNoText(
                **blob.model_dump(),
                metadata=InfoBlobMetadata(**blob.model_dump()),
            )
            for blob in info_blobs
        ],
        model=completion_model,
    )


async def ask_assistant(
    ask: AskAssistant,
    runner: AssistantGuardRunner,
    db_session: AsyncSession,
    session: Optional[SessionInDB] = None,
):
    if ask.stream:
        response = await runner.run(
            ask.question, file_ids=ask.files, session=session, stream=True
        )

        @gen_transaction(db_session)
        async def event_stream():
            async for chunk in response.answer:
                yield to_ask_reponse(
                    question=response.question,
                    files=response.files,
                    session=response.session,
                    answer=chunk,
                    info_blobs=response.info_blobs,
                    completion_model=response.completion_model,
                ).model_dump_json()

        return EventSourceResponse(event_stream())

    response = await runner.run(
        ask.question, file_ids=ask.files, session=session, stream=False
    )

    return to_ask_reponse(
        question=response.question,
        files=response.files,
        session=response.session,
        answer=response.answer,
        info_blobs=response.info_blobs,
        completion_model=response.completion_model,
    )
