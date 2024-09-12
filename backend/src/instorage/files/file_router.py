# MIT license

from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile

from instorage.files.file_models import FilePublic
from instorage.main.container.container import Container
from instorage.main.models import PaginatedResponse
from instorage.server import protocol
from instorage.server.dependencies.container import get_container
from instorage.server.protocol import responses

router = APIRouter()


@router.post(
    "/", response_model=FilePublic, responses=responses.get_responses([415, 413])
)
async def upload_file(
    upload_file: UploadFile,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.file_service()
    return await service.save_file(upload_file)


@router.get(
    "/",
    response_model=PaginatedResponse[FilePublic],
    status_code=200,
)
async def get_files(
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.file_service()
    files = await service.get_files()

    return protocol.to_paginated_response(
        [FilePublic(**item.model_dump()) for item in files]
    )


@router.delete("/{id}/", status_code=204)
async def delete_file(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.file_service()
    await service.delete_file(id)
