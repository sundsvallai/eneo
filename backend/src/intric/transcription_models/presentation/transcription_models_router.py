from uuid import UUID

from fastapi import APIRouter, Depends

from intric.main.container.container import Container
from intric.main.models import PaginatedResponse
from intric.server.dependencies.container import get_container
from intric.server.protocol import responses
from intric.transcription_models.presentation.transcription_model_models import (
    TranscriptionModelPublic,
    TranscriptionModelUpdate,
)

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[TranscriptionModelPublic],
)
async def get_transcription_models(
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.transcription_model_crud_service()

    models = await service.get_transcription_models()

    return PaginatedResponse(
        items=[TranscriptionModelPublic.from_domain(model) for model in models]
    )


@router.post(
    "/{id}/",
    response_model=TranscriptionModelPublic,
    responses=responses.get_responses([404]),
)
async def update_transcription_model(
    id: UUID,
    update_flags: TranscriptionModelUpdate,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.transcription_model_crud_service()

    transcription_model = await service.update_transcription_model(
        model_id=id,
        is_org_enabled=update_flags.is_org_enabled,
        is_org_default=update_flags.is_org_default,
        security_classification=update_flags.security_classification,
    )

    return TranscriptionModelPublic.from_domain(transcription_model)
