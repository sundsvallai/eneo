from typing import Optional

from sse_starlette import EventSourceResponse

from instorage.ai_models.completion_models.llms import CompletionModel
from instorage.assistants.assistant import (
    AskAssistant,
    AssistantGuard,
    AssistantInDBWithUser,
    AssistantPublicWithUser,
)
from instorage.assistants.assistant_runner import AssistantRunner
from instorage.database.database import AsyncSession
from instorage.database.transaction import gen_transaction
from instorage.groups.group import GroupPublic
from instorage.info_blobs.info_blob import (
    InfoBlobInDB,
    InfoBlobMetadata,
    InfoBlobPublicNoText,
)
from instorage.server import protocol
from instorage.sessions.session import AskResponse, SessionInDB
from instorage.workflows.workflow import StepInDB


def from_domain_assistant(
    assistant: AssistantInDBWithUser, guard_step: StepInDB = None
):
    assistant_public = AssistantPublicWithUser(
        **assistant.model_dump(exclude={"id", "groups"}),
        id=assistant.uuid,
        groups=[protocol.to_uuid(group, GroupPublic) for group in assistant.groups],
    )

    if guard_step is not None:
        assistant_public.guardrail = AssistantGuard(
            guardrail_active=assistant.guardrail_active,
            guardrail_string=guard_step.service.prompt,
            on_fail_message=guard_step.filter.chain_breaker_message,
        )
    elif assistant.guard_step is not None:
        assistant_public.guardrail = AssistantGuard(
            guardrail_active=assistant.guardrail_active,
            guardrail_string=assistant.guard_step.service.prompt,
            on_fail_message=assistant.guard_step.filter.chain_breaker_message,
        )

    return assistant_public


def from_domain_assistants(assistants: list[AssistantInDBWithUser]):
    return [from_domain_assistant(assistant) for assistant in assistants]


def to_assistant_with_user(assistant: AssistantInDBWithUser):
    return AssistantPublicWithUser(
        **from_domain_assistant(assistant).model_dump(),
    )


def to_assistants_with_user(assistants: list[AssistantInDBWithUser]):
    return [to_assistant_with_user(assistant) for assistant in assistants]


def to_ask_reponse(
    session: SessionInDB,
    chunk: str,
    info_blobs: list[InfoBlobInDB],
    model: Optional[CompletionModel] = None,
):
    return AskResponse(
        session_id=session.uuid,
        answer=chunk,
        references=[
            InfoBlobPublicNoText(
                **blob.model_dump(exclude={"group_id"}),
                group_id=blob.group.uuid,
                metadata=InfoBlobMetadata(**blob.model_dump()),
            )
            for blob in info_blobs
        ],
        model=model,
    )


async def ask_assistant(
    ask: AskAssistant,
    runner: AssistantRunner,
    db_session: AsyncSession,
    session: Optional[SessionInDB] = None,
):
    if ask.stream:
        response = await runner.run(ask.question, session=session, stream=True)

        @gen_transaction(db_session)
        async def event_stream():
            async for chunk in response.answer:
                yield to_ask_reponse(
                    response.session, chunk, response.info_blobs, response.model
                ).model_dump_json()

        return EventSourceResponse(event_stream())

    response = await runner.run(ask.question, session=session, stream=False)

    return to_ask_reponse(
        response.session, response.answer, response.info_blobs, response.model
    )
