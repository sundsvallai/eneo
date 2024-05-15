import asyncio
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile

from instorage.ai_models.embedding_models.datastore import datastore_factory
from instorage.ai_models.embedding_models.datastore.datastore import Datastore
from instorage.authentication.auth_dependencies import get_current_active_user
from instorage.groups import group_protocol
from instorage.groups.group import (
    CreateGroupRequest,
    DeleteGroupResponse,
    GroupPublicWithMetadata,
    GroupUpdatePublic,
)
from instorage.groups.group_factory import get_groups_service
from instorage.groups.group_service import GroupService
from instorage.info_blobs import info_blob_factory, info_blob_protocol
from instorage.info_blobs.file.file_service import FileService
from instorage.info_blobs.file.text import TextExtractor
from instorage.info_blobs.info_blob import (
    InfoBlobAdd,
    InfoBlobPublic,
    InfoBlobPublicNoText,
)
from instorage.info_blobs.info_blob_service import InfoBlobService
from instorage.jobs import job_factory
from instorage.jobs.job_models import JobPublic
from instorage.jobs.task_service import TaskService
from instorage.main.exceptions import BadRequestException
from instorage.main.models import PaginatedResponse, PaginatedResponseWithPublicItems
from instorage.server import protocol
from instorage.server.models.api import InfoBlobUpsertRequest
from instorage.server.protocol import responses
from instorage.users.user import UserInDB

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponseWithPublicItems[GroupPublicWithMetadata],
)
async def get_groups(
    include_public: bool = False,
    service: GroupService = Depends(get_groups_service),
):
    """If `include_public`, return all public groups of the tenant"""

    groups = await service.get_user_groups()
    counts = await service.get_counts_for_groups(groups)
    groups_public = group_protocol.to_groups_public_with_metadata(groups, counts)

    if include_public:
        public_groups = await service.get_public_groups()
        public_groups_counts = await service.get_counts_for_groups(public_groups)
        public_groups_public = group_protocol.to_groups_public_with_metadata(
            public_groups, public_groups_counts
        )
    else:
        public_groups_public = []

    return protocol.to_paginated_response_with_public(
        groups_public, public_groups_public
    )


@router.get(
    "/public/",
    response_model=PaginatedResponse[GroupPublicWithMetadata],
    deprecated=True,
)
async def get_public_groups(service: GroupService = Depends(get_groups_service)):
    """Returns the public groups of the tenant as well."""

    groups = await service.get_public_groups()
    counts = await service.get_counts_for_groups(groups)

    groups_public = [
        group_protocol.to_group_public_with_metadata(group, count)
        for group, count in zip(groups, counts)
    ]

    return protocol.to_paginated_response(groups_public)


@router.get(
    "/{id}/",
    response_model=GroupPublicWithMetadata,
    responses=responses.get_responses([404]),
)
async def get_group_by_id(
    id: UUID, service: GroupService = Depends(get_groups_service)
):
    group = await service.get_group_by_uuid(id)
    count = await service.get_count_for_group(group)

    return group_protocol.to_group_public_with_metadata(group, count)


@router.post("/", response_model=GroupPublicWithMetadata)
async def create_group(
    group: CreateGroupRequest,
    service: GroupService = Depends(get_groups_service),
):
    """
    Valid values for `embedding_model` are the provided by `GET /api/v1/settings/models/`.
    Use the `name` field of the response from this endpoint.
    """
    group = await service.create_group(group)

    return group_protocol.to_group_public_with_metadata(group, 0)


@router.post(
    "/{id}/",
    response_model=GroupPublicWithMetadata,
    responses=responses.get_responses([404]),
)
async def update_group(
    id: UUID,
    group: GroupUpdatePublic,
    service: GroupService = Depends(get_groups_service),
):
    group_updated = await service.update_group(group, id)
    count = await service.get_count_for_group(group_updated)

    return group_protocol.to_group_public_with_metadata(group_updated, count)


@router.delete(
    "/{id}/",
    response_model=DeleteGroupResponse,
    responses=responses.get_responses([404]),
)
async def delete_group_by_id(
    id: UUID, service: GroupService = Depends(get_groups_service)
):
    group_deleted, success, count = await service.delete_group(id)

    return group_protocol.to_deletion_response(group_deleted, count, success)


@router.post(
    "/{id}/info-blobs/",
    response_model=PaginatedResponse[InfoBlobPublic],
    responses=responses.get_responses([400, 404, 403, 503]),
)
async def add_info_blobs(
    id: UUID,
    info_blobs: InfoBlobUpsertRequest,
    service: InfoBlobService = Depends(info_blob_factory.get_info_blob_service),
    current_user: UserInDB = Depends(get_current_active_user),
    datastore: Datastore = Depends(datastore_factory.get_datastore),
):
    """Maximum allowed simultaneous upload is 128.

    Will be embedded using the embedding model of the group.
    """
    if len(info_blobs.info_blobs) > 128:
        raise BadRequestException("Too many info-blobs!")

    info_blobs_to_add = [
        InfoBlobAdd(
            **blob.model_dump(),
            **blob.metadata.model_dump() if blob.metadata else {},
            user_id=current_user.id,
            group_id=id,
        )
        for blob in info_blobs.info_blobs
    ]

    info_blobs_added = await service.add_info_blobs(info_blobs_to_add)

    # Add to datastore
    for info_blob in info_blobs_added:
        await datastore.add(info_blob)

    info_blobs_public = [
        info_blob_protocol.to_info_blob_public(blob) for blob in info_blobs_added
    ]

    return protocol.to_paginated_response(info_blobs_public)


@router.get(
    "/{id}/info-blobs/",
    response_model=PaginatedResponse[InfoBlobPublicNoText],
    responses=responses.get_responses([400, 404]),
)
async def get_info_blobs(
    id: UUID,
    service: InfoBlobService = Depends(info_blob_factory.get_info_blob_service),
):
    info_blobs_in_db = await service.get_by_group(id)

    info_blobs_public = [
        info_blob_protocol.to_info_blob_public_no_text(blob)
        for blob in info_blobs_in_db
    ]

    return protocol.to_paginated_response(info_blobs_public)


@router.post(
    "/{id}/info-blobs/upload-files/",
    response_model=PaginatedResponse[InfoBlobPublic],
    responses=responses.get_responses([400, 403, 404, 503]),
    deprecated=True,
)
async def upload_files(
    id: UUID,
    files: list[UploadFile] = File(...),
    service: InfoBlobService = Depends(info_blob_factory.get_info_blob_service),
    current_user: UserInDB = Depends(get_current_active_user),
    datastore: Datastore = Depends(datastore_factory.get_datastore),
):
    """Adds an info-blob from files. Supported file types: txt, docx, md, pdf, csv.

    Maximum allowed simultaneous upload is 128.
    Maximum total file size is 2MB.

    Will be embedded using the embedding model of the group.
    """

    # File validation
    if len(files) > 128:
        raise BadRequestException("Too many files!")

    file_service = FileService()
    await asyncio.to_thread(file_service.validate_file_types, files)
    await asyncio.to_thread(file_service.validate_file_sizes, files)

    info_blobs_upsert = [
        InfoBlobAdd(
            title=file.filename,
            user_id=current_user.id,
            text=await TextExtractor(file.file).extract(),
            group_id=id,
        )
        for file in files
    ]

    info_blobs_in_db = await service.add_info_blobs(info_blobs_upsert)

    # Add to datastore
    for info_blob in info_blobs_in_db:
        await datastore.add(info_blob)

    info_blobs_public = [
        info_blob_protocol.to_info_blob_public(blob) for blob in info_blobs_in_db
    ]

    return protocol.to_paginated_response(info_blobs_public)


@router.post(
    "/{id}/info-blobs/upload/",
    response_model=JobPublic,
    status_code=202,
)
async def upload_file(
    id: UUID,
    file: UploadFile,
    task_service: TaskService = Depends(job_factory.get_task_service),
):
    """Starts a job, use the job operations to keep track of this job"""

    return await task_service.queue_upload_file(
        id, file.file, file.content_type, file.filename
    )
