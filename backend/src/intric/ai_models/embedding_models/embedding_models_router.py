# MIT License

from uuid import UUID

from fastapi import APIRouter, Depends

from intric.ai_models.embedding_models.embedding_model import (
    EmbeddingModelPublic,
    EmbeddingModelUpdateFlags,
)
from intric.main.container.container import Container
from intric.main.models import PaginatedResponse
from intric.server import protocol
from intric.server.dependencies.container import get_container
from intric.server.protocol import responses

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[EmbeddingModelPublic],
)
async def get_embedding_models(
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.ai_models_service()

    models = await service.get_embedding_models()

    return protocol.to_paginated_response(models)


@router.post(
    "/{id}/",
    response_model=EmbeddingModelPublic,
    responses=responses.get_responses([404]),
)
async def enable_embedding_model(
    id: UUID,
    data: EmbeddingModelUpdateFlags,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.ai_models_service()
    return await service.enable_embedding_model(embedding_model_id=id, data=data)
