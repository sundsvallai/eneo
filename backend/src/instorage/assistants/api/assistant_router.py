from uuid import UUID

from fastapi import APIRouter, Depends

from instorage.assistants.api import assistant_protocol
from instorage.assistants.api.assistant_models import (
    AskAssistant,
    AssistantCreatePublic,
    AssistantPublic,
    AssistantUpdatePublic,
)
from instorage.assistants.assistant_runner_factory import get_assistant_guard_runner
from instorage.authentication.auth_models import ApiKey
from instorage.database.database import AsyncSession, get_session
from instorage.main.container.container import Container
from instorage.main.models import PaginatedResponse
from instorage.server import protocol
from instorage.server.dependencies.container import get_container
from instorage.server.protocol import responses
from instorage.sessions import sessions_factory
from instorage.sessions.session import (
    AskResponse,
    SessionFeedback,
    SessionMetadataPublic,
    SessionPublic,
)
from instorage.sessions.session_protocol import (
    to_session_metadata_public,
    to_session_public,
)
from instorage.sessions.session_service import SessionService
from instorage.spaces.api.space_models import TransferApplicationRequest
from instorage.workflows.assistant_guard_runner import AssistantGuardRunner

router = APIRouter()


@router.post(
    "/",
    response_model=AssistantPublic,
    responses=responses.get_responses([404]),
)
async def create_assistant(
    assistant: AssistantCreatePublic,
    container: Container = Depends(get_container(with_user=True)),
):

    service = container.assistant_service()
    assembler = container.assistant_assembler()

    assistant = await service.create_assistant(
        name=assistant.name,
        prompt=assistant.prompt,
        completion_model_kwargs=assistant.completion_model_kwargs,
        logging_enabled=assistant.logging_enabled,
        groups=[group.id for group in assistant.groups],
        websites=[website.id for website in assistant.websites],
        completion_model_id=assistant.completion_model.id,
    )

    return assembler.from_assistant_to_model(assistant)


@router.get("/", response_model=PaginatedResponse[AssistantPublic])
async def get_assistants(
    name: str = None,
    for_tenant: bool = False,
    container: Container = Depends(get_container(with_user=True)),
):
    """Requires Admin permission if `for_tenant` is `true`."""
    service = container.assistant_service()
    assembler = container.assistant_assembler()

    assistants = await service.get_assistants(name, for_tenant)

    assistants = [
        assembler.from_assistant_to_model(assistant) for assistant in assistants
    ]

    return protocol.to_paginated_response(assistants)


@router.get(
    "/{id}/",
    response_model=AssistantPublic,
    responses=responses.get_responses([400, 404]),
)
async def get_assistant(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.assistant_service()
    assembler = container.assistant_assembler()

    return assembler.from_assistant_to_model(await service.get_assistant(id))


@router.post(
    "/{id}/",
    response_model=AssistantPublic,
    responses=responses.get_responses([400, 404]),
)
async def update_assistant(
    id: UUID,
    assistant: AssistantUpdatePublic,
    container: Container = Depends(get_container(with_user=True)),
):
    """Omitted fields are not updated"""
    service = container.assistant_service()
    assembler = container.assistant_assembler()

    groups = None
    if assistant.groups is not None:
        groups = [group.id for group in assistant.groups]

    websites = None
    if assistant.websites is not None:
        websites = [website.id for website in assistant.websites]

    completion_model_id = None
    if assistant.completion_model is not None:
        completion_model_id = assistant.completion_model.id

    completion_model_kwargs = None
    if assistant.completion_model_kwargs is not None:
        completion_model_kwargs = assistant.completion_model_kwargs

    assistant = await service.update_assistant(
        id=id,
        name=assistant.name,
        prompt=assistant.prompt,
        completion_model_id=completion_model_id,
        completion_model_kwargs=completion_model_kwargs,
        logging_enabled=assistant.logging_enabled,
        groups=groups,
        websites=websites,
    )

    return assembler.from_assistant_to_model(assistant)


@router.delete(
    "/{id}/",
    status_code=204,
    responses=responses.get_responses([403, 404]),
)
async def delete_assistant(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.assistant_service()
    await service.delete_assistant(id)


@router.post(
    "/{id}/sessions/",
    response_model=AskResponse,
    responses=responses.streaming_response(AskResponse, [400, 404]),
)
async def ask_assistant(
    ask: AskAssistant,
    runner: AssistantGuardRunner = Depends(get_assistant_guard_runner),
    db_session: AsyncSession = Depends(get_session),
):
    """Streams the response as Server-Sent Events if stream == true"""

    return await assistant_protocol.ask_assistant(
        ask=ask, runner=runner, db_session=db_session
    )


@router.get(
    "/{id}/sessions/",
    response_model=PaginatedResponse[SessionMetadataPublic],
    responses=responses.get_responses([400, 404]),
)
async def get_assistant_sessions(
    id: UUID,
    session_service: SessionService = Depends(sessions_factory.get_session_service),
    container: Container = Depends(get_container(with_user=True)),
):
    assistant_service = container.assistant_service()
    assistant_in_db = await assistant_service.get_assistant(id)
    sessions = await session_service.get_sessions_by_assistant(assistant_in_db.id)

    sessions_public = [to_session_metadata_public(session) for session in sessions]

    return {"count": len(sessions), "items": sessions_public}


@router.get(
    "/{id}/sessions/{session_id}/",
    response_model=SessionPublic,
    responses=responses.get_responses([400, 404]),
)
async def get_assistant_session(
    id: UUID,
    session_id: UUID,
    session_service: SessionService = Depends(sessions_factory.get_session_service),
):
    session = await session_service.get_session_by_uuid(session_id, assistant_id=id)

    return to_session_public(session)


@router.delete(
    "/{id}/sessions/{session_id}/",
    response_model=SessionPublic,
    responses=responses.get_responses([400, 404]),
)
async def delete_assistant_session(
    id: UUID,
    session_id: UUID,
    session_service: SessionService = Depends(sessions_factory.get_session_service),
):
    session = await session_service.delete(session_id, assistant_id=id)

    return to_session_public(session)


@router.post(
    "/{id}/sessions/{session_id}/",
    response_model=AskResponse,
    responses=responses.streaming_response(AskResponse, [400, 404]),
)
async def ask_followup(
    id: UUID,
    session_id: UUID,
    ask: AskAssistant,
    runner: AssistantGuardRunner = Depends(get_assistant_guard_runner),
    session_service: SessionService = Depends(
        sessions_factory.get_session_service_from_assistant_api_key
    ),
    db_session: AsyncSession = Depends(get_session),
):
    """Streams the response as Server-Sent Events if stream == true"""
    session = await session_service.get_session_by_uuid(session_id, assistant_id=id)

    return await assistant_protocol.ask_assistant(
        ask=ask, runner=runner, db_session=db_session, session=session
    )


@router.post(
    "/{id}/sessions/{session_id}/feedback/",
    response_model=SessionPublic,
    responses=responses.get_responses([400, 404]),
)
async def leave_feedback(
    id: UUID,
    session_id: UUID,
    feedback: SessionFeedback,
    session_service: SessionService = Depends(
        sessions_factory.get_session_service_from_assistant_api_key
    ),
):
    session = await session_service.leave_feedback(
        session_id=session_id, assistant_id=id, feedback=feedback
    )

    return to_session_public(session)


@router.get("/{id}/api-keys/", response_model=ApiKey)
async def generate_read_only_assistant_key(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
):
    """Generates a read-only api key for this assistant.

    This api key can only be used on `POST /api/v1/assistants/{id}/sessions/`
    and `POST /api/v1/assistants/{id}/sessions/{session_id}/`."""
    service = container.assistant_service()
    return await service.generate_api_key(id)


@router.post("/{id}/transfer/", status_code=204)
async def transfer_assistant_to_space(
    id: UUID,
    transfer_req: TransferApplicationRequest,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.assistant_service()
    await service.move_assistant_to_space(
        assistant_id=id,
        space_id=transfer_req.target_space_id,
        move_resources=transfer_req.move_resources,
    )
