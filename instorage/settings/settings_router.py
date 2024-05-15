from fastapi import APIRouter, Depends

from instorage.authentication import auth_dependencies
from instorage.info_blobs.file.text import AUDIO_FILE_TYPES, TextMimeTypes
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
def get_models(
    service: SettingService = Depends(settings_factory.get_settings_service),
):
    """Use the `name` field in the response as values for `completion_model`
    and `embedding_model` in creating and updating
      `Assistants` and `Services`.
    """

    completion_models = service.get_available_completion_models()
    embedding_models = service.get_available_embedding_models()

    return GetModelsResponse(
        completion_models=completion_models, embedding_models=embedding_models
    )


@router.get(
    "/formats/",
    response_model=PaginatedResponse[str],
    dependencies=[Depends(auth_dependencies.get_current_active_user)],
)
def get_formats():
    return to_paginated_response(TextMimeTypes.values() + AUDIO_FILE_TYPES)
