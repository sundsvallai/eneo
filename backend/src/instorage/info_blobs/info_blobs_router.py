from fastapi import APIRouter, Depends, Path

from instorage.authentication.auth_dependencies import get_current_active_user
from instorage.info_blobs import info_blob_factory
from instorage.info_blobs.info_blob import (
    InfoBlobPublic,
    InfoBlobPublicNoText,
    InfoBlobUpdate,
    InfoBlobUpdatePublic,
)
from instorage.info_blobs.info_blob_protocol import (
    to_info_blob_public,
    to_info_blob_public_no_text,
)
from instorage.info_blobs.info_blob_service import InfoBlobService
from instorage.main.logging import get_logger
from instorage.main.models import PaginatedResponse
from instorage.server import protocol
from instorage.server.protocol import responses
from instorage.users.user import UserInDB

logger = get_logger(__name__)

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[InfoBlobPublicNoText],
)
async def get_info_blob_ids(
    service: InfoBlobService = Depends(info_blob_factory.get_info_blob_service),
):
    """Returns a list of info-blobs.

    Does not return the text of each info-blob, 'text' will be null.
    """
    info_blobs_in_db = await service.get_by_user()

    info_blobs_public = [to_info_blob_public_no_text(blob) for blob in info_blobs_in_db]

    return protocol.to_paginated_response(info_blobs_public)


@router.get(
    "/{id}/",
    response_model=InfoBlobPublic,
    responses=responses.get_responses([404]),
)
async def get_info_blob(
    id: str = Path(...),
    service: InfoBlobService = Depends(info_blob_factory.get_info_blob_service),
):
    info_blob_in_db = await service.get_by_id(id)

    return to_info_blob_public(info_blob_in_db)


@router.post(
    "/{id}/",
    response_model=InfoBlobPublic,
    responses=responses.get_responses([404]),
)
async def update_info_blob(
    id: str,
    info_blob: InfoBlobUpdatePublic,
    service: InfoBlobService = Depends(info_blob_factory.get_info_blob_service),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """Omitted fields are not updated."""

    info_blob_upsert = InfoBlobUpdate(
        id=id,
        **info_blob.metadata.model_dump(),
        user_id=current_user.id,
    )

    updated_blob = await service.update_info_blob(info_blob_upsert)

    return to_info_blob_public(updated_blob)


@router.delete(
    "/{id}/",
    response_model=InfoBlobPublic,
    responses=responses.get_responses([404]),
)
async def delete_info_blob(
    id: str = Path(...),
    service: InfoBlobService = Depends(info_blob_factory.get_info_blob_service),
):
    """Returns the deleted object."""
    info_blob_deleted = await service.delete(id)

    return to_info_blob_public(info_blob_deleted)
