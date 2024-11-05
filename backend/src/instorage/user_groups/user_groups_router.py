# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

from uuid import UUID

from fastapi import APIRouter, Depends

from instorage.main.models import PaginatedResponse
from instorage.server.protocol import responses, to_paginated_response
from instorage.user_groups.user_group import (
    UserGroupCreateRequest,
    UserGroupPublic,
    UserGroupUpdateRequest,
)
from instorage.user_groups.user_groups_factory import get_user_groups_service
from instorage.user_groups.user_groups_service import UserGroupsService

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[UserGroupPublic],
)
async def get_user_groups(
    service: UserGroupsService = Depends(get_user_groups_service),
):
    user_groups = await service.get_all_user_groups()

    return to_paginated_response(user_groups)


@router.get(
    "/{id}/",
    response_model=UserGroupPublic,
    responses=responses.get_responses([404]),
)
async def get_user_group_by_uuid(
    id: UUID, service: UserGroupsService = Depends(get_user_groups_service)
):
    return await service.get_user_group_by_uuid(id)


@router.post("/", response_model=UserGroupPublic)
async def create_user_group(
    user_group: UserGroupCreateRequest,
    service: UserGroupsService = Depends(get_user_groups_service),
):
    return await service.create_user_group(user_group)


@router.post(
    "/{id}/",
    response_model=UserGroupPublic,
    responses=responses.get_responses([404]),
)
async def update_user_group(
    id: UUID,
    user_group: UserGroupUpdateRequest,
    service: UserGroupsService = Depends(get_user_groups_service),
):
    return await service.update_user_group(
        user_group_uuid=id, user_group_update=user_group
    )


@router.delete(
    "/{id}/",
    response_model=UserGroupPublic,
    responses=responses.get_responses([404]),
)
async def delete_user_group_by_uuid(
    id: UUID, service: UserGroupsService = Depends(get_user_groups_service)
):
    return await service.delete_user_group(id)


@router.post(
    "/{id}/users/{user_id}/",
    response_model=UserGroupPublic,
    responses=responses.get_responses([404]),
)
async def add_user_to_user_group(
    id: UUID,
    user_id: UUID,
    service: UserGroupsService = Depends(get_user_groups_service),
):
    return await service.add_user(user_group_uuid=id, user_id=user_id)


@router.delete(
    "/{id}/users/{user_id}/",
    response_model=UserGroupPublic,
    responses=responses.get_responses([404]),
)
async def delete_user_from_user_group(
    id: UUID,
    user_id: UUID,
    service: UserGroupsService = Depends(get_user_groups_service),
):
    return await service.remove_user(user_group_uuid=id, user_id=user_id)
