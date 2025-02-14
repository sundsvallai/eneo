# MIT License

from uuid import UUID

from fastapi import APIRouter, Depends

from intric.completion_models.presentation import (
    CompletionModelPublic,
    CompletionModelUpdateFlags,
)
from intric.main.container.container import Container
from intric.main.models import PaginatedResponse
from intric.server.dependencies.container import get_container
from intric.server.protocol import responses

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[CompletionModelPublic],
)
async def get_completion_models(
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.completion_model_crud_service()
    assembler = container.completion_model_assembler()

    models = await service.get_completion_models()

    return assembler.from_completion_models_to_models(models)


@router.post(
    "/{id}/",
    response_model=CompletionModelPublic,
    responses=responses.get_responses([404]),
)
async def update_completion_model(
    id: UUID,
    update_flags: CompletionModelUpdateFlags,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.completion_model_crud_service()
    assembler = container.completion_model_assembler()

    completion_model = await service.update_completion_model(
        model_id=id,
        is_org_enabled=update_flags.is_org_enabled,
        is_org_default=update_flags.is_org_default,
    )

    return assembler.from_completion_model_to_model(completion_model=completion_model)
