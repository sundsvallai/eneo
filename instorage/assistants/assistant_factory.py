from typing import Callable
from uuid import UUID

from fastapi import Depends, Path

from instorage.ai_models.completion_models.completion_model_service import (
    CompletionModelServiceFactory,
)
from instorage.ai_models.completion_models.llms import get_completion_model
from instorage.ai_models.embedding_models.datastore import datastore_factory
from instorage.assistants.assistant import AssistantInDBWithUser
from instorage.assistants.assistant_repo import AssistantRepository
from instorage.assistants.assistant_runner import AssistantRunner, RunnerDelegate
from instorage.assistants.assistant_service import AssistantService
from instorage.authentication.auth_dependencies import (
    get_current_active_user,
    get_user_from_token_or_assistant_api_key,
)
from instorage.authentication.auth_factory import get_auth_service
from instorage.authentication.auth_service import AuthService
from instorage.info_blobs.info_blob_chunk_repo import InfoBlobChunkRepo
from instorage.info_blobs.info_blob_repo import InfoBlobRepository
from instorage.main.logging import get_logger
from instorage.questions.questions_repo import QuestionRepository
from instorage.server.dependencies.db import get_repository
from instorage.services.service_factory import get_service_runner
from instorage.services.service_repo import ServiceRepository
from instorage.sessions import sessions_factory
from instorage.sessions.session_service import SessionService
from instorage.users.user import UserInDB
from instorage.users.user_factory import get_user_service
from instorage.users.user_service import UserService
from instorage.workflows.assistant_guard_runner import AssistantGuardRunner
from instorage.workflows.filters import ContinuationFilter
from instorage.workflows.step_repo import StepRepository
from instorage.workflows.steps import Step

logger = get_logger(__name__)


def get_assistants_service(get_user: Callable = get_current_active_user):
    def _get_assistants_service(
        user: UserInDB = Depends(get_user),
        repo: AssistantRepository = Depends(get_repository(AssistantRepository)),
        auth_service: AuthService = Depends(get_auth_service),
        step_repo: StepRepository = Depends(get_repository(StepRepository)),
        service_repo: ServiceRepository = Depends(get_repository(ServiceRepository)),
    ):
        return AssistantService(
            repo=repo,
            user=user,
            auth_service=auth_service,
            service_repo=service_repo,
            step_repo=step_repo,
        )

    return _get_assistants_service


def get_assistant_guard_runner(
    get_user: Callable = get_user_from_token_or_assistant_api_key,
):
    async def _get_assistant_guard_runner(
        id: UUID = Path(),
        assistant_service: AssistantService = Depends(get_assistants_service(get_user)),
        user_service: UserService = Depends(get_user_service),
        info_blob_repo: InfoBlobRepository = Depends(
            get_repository(InfoBlobRepository)
        ),
        user: UserInDB = Depends(get_user),
        session_service: SessionService = Depends(
            sessions_factory.get_session_service(get_user)
        ),
        question_repo: QuestionRepository = Depends(get_repository(QuestionRepository)),
        info_blob_chunk_repo: InfoBlobChunkRepo = Depends(
            get_repository(InfoBlobChunkRepo)
        ),
    ):
        # Get assistant specification
        assistant = await assistant_service.get_assistant(id)

        return await get_guard_runner(
            assistant=assistant,
            user_service=user_service,
            info_blob_repo=info_blob_repo,
            user=user,
            session_service=session_service,
            question_repo=question_repo,
            info_blob_chunk_repo=info_blob_chunk_repo,
        )

    return _get_assistant_guard_runner


async def get_guard_runner(
    assistant: AssistantInDBWithUser,
    user_service: UserService,
    info_blob_repo: InfoBlobRepository,
    user: UserInDB,
    session_service: SessionService,
    question_repo: QuestionRepository,
    info_blob_chunk_repo: InfoBlobChunkRepo,
):
    assistant_runner = await get_assistant_runner(
        assistant=assistant,
        user_service=user_service,
        info_blob_repo=info_blob_repo,
        user=user,
        session_service=session_service,
        info_blob_chunk_repo=info_blob_chunk_repo,
    )

    if not assistant.guardrail_active:
        guard_step = None
    else:
        guard_service_runner = await get_service_runner(
            assistant.guard_step.service,
            user_service=user_service,
            user=user,
            question_repo=question_repo,
            info_blob_repo=info_blob_repo,
            with_groups=assistant.groups,
            info_blob_chunk_repo=info_blob_chunk_repo,
        )
        guard_filter = ContinuationFilter(
            chain_breaker_message=assistant.guard_step.filter.chain_breaker_message
        )
        guard_step = Step(runner=guard_service_runner, filter=guard_filter)

    return AssistantGuardRunner(
        assistant_runner, session_service=session_service, guard_step=guard_step
    )


async def get_assistant_runner(
    assistant: AssistantInDBWithUser,
    user_service: UserService,
    info_blob_repo: InfoBlobRepository,
    user: UserInDB,
    session_service: SessionService,
    info_blob_chunk_repo: InfoBlobChunkRepo,
):
    # Get completion model service
    completion_model = get_completion_model(assistant.completion_model)
    completion_model_service = await CompletionModelServiceFactory.create(
        completion_model,
        assistant.completion_model_kwargs,
        user_service,
        user,
    )

    # Get embedder
    if assistant.groups:
        embedding_model_name = assistant.groups[0].embedding_model
        datastore = datastore_factory.get_datastore_from_model_string(
            embedding_model_name, info_blob_chunk_repo=info_blob_chunk_repo
        )

    else:
        datastore = None

    runner_delegate = RunnerDelegate(
        info_blobs_repo=info_blob_repo, datastore=datastore, groups=assistant.groups
    )

    runner = AssistantRunner(
        assistant=assistant,
        session_service=session_service,
        completion_model_service=completion_model_service,
        runner_delegate=runner_delegate,
        completion_model=completion_model,
    )

    return runner
