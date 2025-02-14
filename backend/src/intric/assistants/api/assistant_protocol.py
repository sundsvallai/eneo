from typing import TYPE_CHECKING, Optional

from sse_starlette import EventSourceResponse

from intric.ai_models.completion_models.completion_model import CompletionModel
from intric.database.database import AsyncSession
from intric.database.transaction import gen_transaction
from intric.files.file_models import File, FilePublic
from intric.info_blobs.info_blob import (
    InfoBlobAskAssistantPublic,
    InfoBlobInDB,
    InfoBlobMetadata,
)
from intric.main.logging import get_logger
from intric.questions.question import UseTools
from intric.sessions.session import AskResponse, SessionInDB

if TYPE_CHECKING:
    from intric.assistants.api.assistant_models import AssistantResponse

logger = get_logger(__name__)


def to_ask_response(
    question: str,
    files: list[File],
    session: SessionInDB,
    answer: str,
    info_blobs: list[InfoBlobInDB],
    completion_model: Optional[CompletionModel] = None,
    tools: "UseTools" = None,
):
    return AskResponse(
        question=question,
        files=[FilePublic(**file.model_dump()) for file in files],
        session_id=session.id,
        answer=answer,
        references=[
            InfoBlobAskAssistantPublic(
                **blob.model_dump(),
                metadata=InfoBlobMetadata(**blob.model_dump()),
            )
            for blob in info_blobs
        ],
        model=completion_model,
        tools=tools,
    )


async def to_response(
    response: "AssistantResponse",
    db_session: AsyncSession,
    stream: bool,
):
    if stream:

        @gen_transaction(db_session)
        async def event_stream():
            async for references, chunk in response.answer:
                yield to_ask_response(
                    question=response.question,
                    files=response.files,
                    session=response.session,
                    answer=chunk,
                    info_blobs=references,
                    completion_model=response.completion_model,
                    tools=response.tools,
                ).model_dump_json()

        return EventSourceResponse(event_stream())

    return to_ask_response(
        question=response.question,
        files=response.files,
        session=response.session,
        answer=response.answer,
        info_blobs=response.info_blobs,
        completion_model=response.completion_model,
        tools=response.tools,
    )
