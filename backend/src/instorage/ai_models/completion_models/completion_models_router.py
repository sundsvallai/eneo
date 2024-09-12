# MIT License

from uuid import UUID

from fastapi import APIRouter, Depends

from instorage.ai_models.ai_models_factory import get_ai_models_service
from instorage.ai_models.ai_models_service import AIModelsService
from instorage.ai_models.completion_models.completion_model import (
    CompletionModelPublic,
    CompletionModelUpdateFlags,
)
from instorage.main.models import PaginatedResponse
from instorage.server import protocol
from instorage.server.protocol import responses

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[CompletionModelPublic],
)
async def get_completion_models(
    service: AIModelsService = Depends(get_ai_models_service),
):
    models = await service.get_completion_models()

    return protocol.to_paginated_response(models)


@router.post(
    "/{id}/",
    response_model=CompletionModelPublic,
    responses=responses.get_responses([404]),
)
async def enable_completion_model(
    id: UUID,
    data: CompletionModelUpdateFlags,
    service: AIModelsService = Depends(get_ai_models_service),
):
    return await service.enable_completion_model(completion_model_id=id, data=data)
