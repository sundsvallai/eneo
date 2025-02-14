from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile

from intric.ai_models.embedding_models.datastore import datastore_factory
from intric.ai_models.embedding_models.datastore.datastore import Datastore
from intric.ai_models.embedding_models.datastore.datastore_models import (
    SemanticSearchRequest,
    SemanticSearchResponse,
)
from intric.authentication.auth_dependencies import get_current_active_user
from intric.groups.api import group_protocol
from intric.groups.api.group_models import (
    CreateGroupRequest,
    DeleteGroupResponse,
    GroupPublicWithMetadata,
    GroupUpdatePublic,
)
from intric.info_blobs import info_blob_protocol
from intric.info_blobs.info_blob import (
    InfoBlobAdd,
    InfoBlobPublic,
    InfoBlobPublicNoText,
)
from intric.jobs.job_models import JobPublic
from intric.main.container.container import Container
from intric.main.exceptions import BadRequestException
from intric.main.models import PaginatedResponse
from intric.server import protocol
from intric.server.dependencies.container import get_container
from intric.server.models.api import InfoBlobUpsertRequest
from intric.server.protocol import responses
from intric.spaces.api.space_models import TransferRequest
from intric.users.user import UserInDB

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[GroupPublicWithMetadata],
)
async def get_groups(container: Container = Depends(get_container(with_user=True))):
    service = container.group_service()
    groups = await service.get_groups_for_user()
    counts = await service.get_counts_for_groups(groups)
    groups_public = group_protocol.to_groups_public_with_metadata(groups, counts)

    return protocol.to_paginated_response(groups_public)


@router.get(
    "/{id}/",
    response_model=GroupPublicWithMetadata,
    responses=responses.get_responses([404]),
)
async def get_group_by_id(
    id: UUID, container: Container = Depends(get_container(with_user=True))
):
    service = container.group_service()
    group = await service.get_group(id)
    count = await service.get_count_for_group(group)

    return group_protocol.to_group_public_with_metadata(group, num_info_blobs=count)


@router.post("/", response_model=GroupPublicWithMetadata, deprecated=True)
async def create_group(
    group: CreateGroupRequest,
    container: Container = Depends(get_container(with_user=True)),
):
    """
    Valid values for `embedding_model` are the provided by `GET /api/v1/settings/models/`.
    Use the `name` field of the response from this endpoint.
    """
    service = container.group_service()
    group = await service.create_group(group)

    return group_protocol.to_group_public_with_metadata(group, num_info_blobs=0)


@router.post(
    "/{id}/",
    response_model=GroupPublicWithMetadata,
    responses=responses.get_responses([404]),
)
async def update_group(
    id: UUID,
    group: GroupUpdatePublic,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.group_service()
    group_updated = await service.update_group(group, id)
    count = await service.get_count_for_group(group_updated)

    return group_protocol.to_group_public_with_metadata(
        group_updated, num_info_blobs=count
    )


@router.delete(
    "/{id}/",
    response_model=DeleteGroupResponse,
    responses=responses.get_responses([404]),
)
async def delete_group_by_id(
    id: UUID, container: Container = Depends(get_container(with_user=True))
):
    service = container.group_service()
    group_deleted, count = await service.delete_group(id)

    return group_protocol.to_deletion_response(group_deleted, count)


@router.post(
    "/{id}/info-blobs/",
    response_model=PaginatedResponse[InfoBlobPublic],
    responses=responses.get_responses([400, 404, 403, 503]),
)
async def add_info_blobs(
    id: UUID,
    info_blobs: InfoBlobUpsertRequest,
    container: Container = Depends(get_container(with_user=True)),
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
            tenant_id=current_user.tenant_id
        )
        for blob in info_blobs.info_blobs
    ]

    service = container.info_blob_service()
    info_blobs_added = await service.add_info_blobs(
        group_id=id, info_blobs=info_blobs_to_add
    )

    # Add to datastore
    info_blobs_updated = []
    for info_blob in info_blobs_added:
        await datastore.add(info_blob)
        info_blob_updated = await service.update_info_blob_size(info_blob.id)
        info_blobs_updated.append(info_blob_updated)

    info_blobs_public = [
        info_blob_protocol.to_info_blob_public(blob) for blob in info_blobs_updated
    ]

    return protocol.to_paginated_response(info_blobs_public)


@router.get(
    "/{id}/info-blobs/",
    response_model=PaginatedResponse[InfoBlobPublicNoText],
    responses=responses.get_responses([400, 404]),
)
async def get_info_blobs(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.info_blob_service()
    info_blobs_in_db = await service.get_by_group(id)

    info_blobs_public = [
        info_blob_protocol.to_info_blob_public_no_text(blob)
        for blob in info_blobs_in_db
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
    container: Container = Depends(get_container(with_user=True)),
):
    """Starts a job, use the job operations to keep track of this job"""

    group_service = container.group_service()

    return await group_service.add_file_to_group(
        group_id=id, file=file.file, mimetype=file.content_type, filename=file.filename
    )


@router.post(
    "/{id}/searches/",
    response_model=PaginatedResponse[SemanticSearchResponse],
)
async def run_semantic_search(
    id: UUID,
    search_parameters: SemanticSearchRequest,
    datastore: Datastore = Depends(datastore_factory.get_datastore),
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.group_service()
    group = await service.get_group(id)

    results = await datastore.semantic_search(
        **search_parameters.model_dump(), groups=[group]
    )

    return protocol.to_paginated_response(results)


@router.post("/{id}/transfer/", status_code=204)
async def transfer_group_to_space(
    id: UUID,
    transfer_req: TransferRequest,
    container: Container = Depends(get_container(with_user=True)),
):
    service = container.group_service()
    await service.move_group_to_space(
        group_id=id, space_id=transfer_req.target_space_id
    )
