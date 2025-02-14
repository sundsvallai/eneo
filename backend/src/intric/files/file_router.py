from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile

from intric.files.file_models import FilePublic
from intric.main.container.container import Container
from intric.main.models import PaginatedResponse
from intric.server import protocol
from intric.server.dependencies.container import get_container
from intric.server.protocol import responses

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


@router.get(
    "/{id}/",
    response_model=FilePublic,
    status_code=200,
)
async def get_file(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.file_service()
    return await service.get_file_by_id(file_id=id)


@router.delete("/{id}/", status_code=204)
async def delete_file(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.file_service()
    await service.delete_file(id)
