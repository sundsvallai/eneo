from fastapi import Depends, Path

from instorage.ai_models.completion_models.completion_model_service import (
    CompletionModelServiceFactory,
)
from instorage.ai_models.completion_models.llms import get_completion_model
from instorage.ai_models.embedding_models.datastore import datastore_factory
from instorage.assistants.assistant_runner import RunnerDelegate
from instorage.authentication.auth_dependencies import get_current_active_user
from instorage.groups.group import GroupInDB
from instorage.groups.group_factory import get_groups_service
from instorage.groups.group_service import GroupService
from instorage.info_blobs.info_blob_chunk_repo import InfoBlobChunkRepo
from instorage.info_blobs.info_blob_repo import InfoBlobRepository
from instorage.questions.questions_repo import QuestionRepository
from instorage.server.dependencies.db import get_repository
from instorage.services.output_parsing.output_parser_factory import OutputParserFactory
from instorage.services.service import ServiceInDBWithUser
from instorage.services.service_repo import ServiceRepository
from instorage.services.service_runner import ServiceRunner
from instorage.services.service_service import ServiceService
from instorage.users.user import UserInDB
from instorage.users.user_factory import get_user_service
from instorage.users.user_service import UserService


def get_services_service(
    user: UserInDB = Depends(get_current_active_user),
    service_repo: ServiceRepository = Depends(get_repository(ServiceRepository)),
    question_repo: QuestionRepository = Depends(get_repository(QuestionRepository)),
    group_service: GroupService = Depends(get_groups_service),
):
    return ServiceService(service_repo, question_repo, group_service, user)


async def get_runner_from_service(
    id: str = Path(),
    service_service: ServiceService = Depends(get_services_service),
    user_service: UserService = Depends(get_user_service),
    user: UserInDB = Depends(get_current_active_user),
    question_repo: QuestionRepository = Depends(get_repository(QuestionRepository)),
    info_blob_repo: InfoBlobRepository = Depends(get_repository(InfoBlobRepository)),
    info_blob_chunk_repo: InfoBlobChunkRepo = Depends(
        get_repository(InfoBlobChunkRepo)
    ),
):
    service = await service_service.get_service(id)

    return await get_service_runner(
        service=service,
        user_service=user_service,
        user=user,
        question_repo=question_repo,
        info_blob_repo=info_blob_repo,
        info_blob_chunk_repo=info_blob_chunk_repo,
    )


async def get_service_runner(
    service: ServiceInDBWithUser,
    user_service: UserService,
    user: UserInDB,
    question_repo: QuestionRepository,
    info_blob_repo: InfoBlobRepository,
    info_blob_chunk_repo: InfoBlobChunkRepo,
    with_groups: list[GroupInDB] = None,
):
    output_parser = OutputParserFactory.create(service)

    prompt = f"{service.prompt}\n{output_parser.get_format_instructions()}"

    # Get completion model service
    completion_model = get_completion_model(service.completion_model)
    completion_model_service = await CompletionModelServiceFactory.create(
        completion_model,
        service.completion_model_kwargs,
        user_service,
        user,
        with_hallucination_guard=False,
    )

    # Get embedder
    if service.groups:
        embedding_model_name = service.groups[0].embedding_model
        datastore = datastore_factory.get_datastore_from_model_string(
            embedding_model_name, info_blob_chunk_repo=info_blob_chunk_repo
        )

    else:
        datastore = None

    runner_delegate = RunnerDelegate(
        info_blobs_repo=info_blob_repo, datastore=datastore, groups=service.groups
    )

    service_runner = ServiceRunner(
        service,
        completion_model_service,
        output_parser,
        runner_delegate=runner_delegate,
        question_repo=question_repo,
        prompt=prompt,
    )

    return service_runner
