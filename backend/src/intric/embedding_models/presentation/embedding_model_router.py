from uuid import UUID

from fastapi import APIRouter, Depends

from intric.embedding_models.presentation.embedding_model_models import (
    EmbeddingModelPublic,
    EmbeddingModelUpdate,
)
from intric.main.container.container import Container
from intric.main.models import PaginatedResponse
from intric.server.dependencies.container import get_container
from intric.server.protocol import responses

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[EmbeddingModelPublic])
async def get_embedding_models(
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.embedding_model_crud_service()
    models = await service.get_embedding_models()

    return PaginatedResponse(items=[EmbeddingModelPublic.from_domain(model) for model in models])


@router.get(
    "/{id}/",
    response_model=EmbeddingModelPublic,
    responses=responses.get_responses([404]),
)
async def get_embedding_model(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.embedding_model_crud_service()
    model = await service.get_embedding_model(model_id=id)

    return EmbeddingModelPublic.from_domain(model)


@router.post(
    "/{id}/",
    response_model=EmbeddingModelPublic,
    responses=responses.get_responses([404]),
)
async def update_embedding_model(
    id: UUID,
    update: EmbeddingModelUpdate,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.embedding_model_crud_service()
    model = await service.update_embedding_model(
        model_id=id,
        is_org_enabled=update.is_org_enabled,
        security_classification=update.security_classification,
    )

    return EmbeddingModelPublic.from_domain(model)
