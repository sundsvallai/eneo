# MIT License

from uuid import UUID

from fastapi import APIRouter, Depends

from instorage.ai_models.ai_models_factory import get_ai_models_service
from instorage.ai_models.ai_models_service import AIModelsService
from instorage.ai_models.embedding_models.embedding_model import (
    EmbeddingModelPublic,
    EmbeddingModelUpdateFlags,
)
from instorage.main.models import PaginatedResponse
from instorage.server import protocol
from instorage.server.protocol import responses

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[EmbeddingModelPublic],
)
async def get_embedding_models(
    service: AIModelsService = Depends(get_ai_models_service),
):
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
    service: AIModelsService = Depends(get_ai_models_service),
):
    return await service.enable_embedding_model(embedding_model_id=id, data=data)
