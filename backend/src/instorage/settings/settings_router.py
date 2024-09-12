from fastapi import APIRouter, Depends

from instorage.authentication import auth_dependencies
from instorage.files.audio import AudioMimeTypes
from instorage.files.image import ImageMimeTypes
from instorage.files.text import TextMimeTypes
from instorage.main.logging import get_logger
from instorage.main.models import PaginatedResponse
from instorage.server.protocol import to_paginated_response
from instorage.settings import settings_factory
from instorage.settings.setting_service import SettingService
from instorage.settings.settings import GetModelsResponse, SettingsPublic

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=SettingsPublic)
async def get_settings(
    service: SettingService = Depends(
        settings_factory.get_settings_service_allowing_read_only_key
    ),
):
    return await service.get_settings()


@router.post("/", response_model=SettingsPublic)
async def upsert_settings(
    settings: SettingsPublic,
    service: SettingService = Depends(settings_factory.get_settings_service),
):
    """Omitted fields are not updated."""

    return await service.update_settings(settings)


@router.get("/models/", response_model=GetModelsResponse)
async def get_models(
    service: SettingService = Depends(settings_factory.get_settings_service),
):
    """
    From the response:
        - use the `id` field as values for `completion_model`
        - use the `id` field as values for `embedding_model`

    in creating and updating `Assistants` and `Services`.
    """

    completion_models = await service.get_available_completion_models()
    embedding_models = await service.get_available_embedding_models()

    return GetModelsResponse(
        completion_models=completion_models, embedding_models=embedding_models
    )


@router.get(
    "/formats/",
    response_model=PaginatedResponse[str],
    dependencies=[Depends(auth_dependencies.get_current_active_user)],
)
def get_formats():
    return to_paginated_response(
        TextMimeTypes.values() + AudioMimeTypes.values() + ImageMimeTypes.values()
    )
