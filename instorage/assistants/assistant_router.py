from uuid import UUID

from fastapi import APIRouter, Depends

from instorage.assistants import assistant_protocol
from instorage.assistants.assistant import (
    AskAssistant,
    AssistantCreatePublic,
    AssistantPublicWithUser,
    AssistantUpdatePublic,
)
from instorage.assistants.assistant_factory import (
    get_assistant_guard_runner,
    get_assistants_service,
)
from instorage.assistants.assistant_runner import AssistantRunner
from instorage.assistants.assistant_service import AssistantService
from instorage.authentication.auth_dependencies import (
    get_user_from_token_or_assistant_api_key,
)
from instorage.authentication.auth_models import ApiKey
from instorage.database.database import AsyncSession
from instorage.main.models import PaginatedResponse, PaginatedResponseWithPublicItems
from instorage.server import protocol
from instorage.server.dependencies.db import get_session
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

router = APIRouter()


@router.post(
    "/",
    response_model=AssistantPublicWithUser,
    responses=responses.get_responses([404]),
)
async def create_assistant(
    assistant: AssistantCreatePublic,
    service: AssistantService = Depends(get_assistants_service()),
):
    """
    Valid values for `completion_model` are the provided by `GET /api/v1/settings/models/`.
    Use the `name` field of the response from this endpoint.
    """

    created_assistant, guard = await service.create_assistant(assistant)

    return assistant_protocol.from_domain_assistant(created_assistant, guard)


@router.get(
    "/", response_model=PaginatedResponseWithPublicItems[AssistantPublicWithUser]
)
async def get_assistants(
    name: str = None,
    include_public: bool = False,
    for_tenant: bool = False,
    service: AssistantService = Depends(get_assistants_service()),
):
    """Requires superuser privileges if `for_tenant` is `true`."""

    assistants = await service.get_assistants(name, for_tenant)

    if include_public:
        public_assistants = await service.get_public_assistants(name)
    else:
        public_assistants = []

    return protocol.to_paginated_response_with_public(
        assistant_protocol.to_assistants_with_user(assistants),
        assistant_protocol.to_assistants_with_user(public_assistants),
    )


@router.get(
    "/{id}/",
    response_model=AssistantPublicWithUser,
    responses=responses.get_responses([400, 404]),
)
async def get_assistant(
    id: UUID, service: AssistantService = Depends(get_assistants_service())
):
    return assistant_protocol.from_domain_assistant(await service.get_assistant(id))


@router.post(
    "/{id}/",
    response_model=AssistantPublicWithUser,
    responses=responses.get_responses([400, 404]),
)
async def update_assistant(
    id: UUID,
    assistant: AssistantUpdatePublic,
    service: AssistantService = Depends(get_assistants_service()),
):
    """Omitted fields are not updated"""

    updated_assistant, guard_step = await service.update_assistant(assistant, id)

    return assistant_protocol.from_domain_assistant(updated_assistant, guard_step)


@router.delete(
    "/{id}/",
    response_model=AssistantPublicWithUser,
    responses=responses.get_responses([400, 404]),
)
async def delete_assistant(
    id: UUID, service: AssistantService = Depends(get_assistants_service())
):
    return assistant_protocol.from_domain_assistant(await service.delete_assistant(id))


@router.post(
    "/{id}/sessions/",
    response_model=AskResponse,
    responses=responses.streaming_response(AskResponse, [400, 404]),
)
async def ask_assistant(
    ask: AskAssistant,
    runner: AssistantRunner = Depends(get_assistant_guard_runner()),
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
    session_service: SessionService = Depends(sessions_factory.get_session_service()),
    assistant_service: AssistantService = Depends(get_assistants_service()),
):
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
    session_service: SessionService = Depends(sessions_factory.get_session_service()),
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
    session_service: SessionService = Depends(sessions_factory.get_session_service()),
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
    runner: AssistantRunner = Depends(get_assistant_guard_runner()),
    session_service: SessionService = Depends(
        sessions_factory.get_session_service(get_user_from_token_or_assistant_api_key)
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
        sessions_factory.get_session_service(get_user_from_token_or_assistant_api_key)
    ),
):
    session = await session_service.leave_feedback(
        session_id=session_id, assistant_id=id, feedback=feedback
    )

    return to_session_public(session)


@router.get("/{id}/api-keys/", response_model=ApiKey)
async def generate_read_only_assistant_key(
    id: UUID, service: AssistantService = Depends(get_assistants_service())
):
    """Generates a read-only api key for this assistant.

    This api key can only be used on `POST /api/v1/assistants/{id}/sessions/`
    and `POST /api/v1/assistants/{id}/sessions/{session_id}/`."""

    return await service.generate_api_key(id)
