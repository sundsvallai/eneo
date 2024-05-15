# MIT License

from uuid import UUID

from fastapi import APIRouter, Depends

from instorage.predefined_roles.predefined_role_factory import (
    get_predefined_roles_service,
)
from instorage.predefined_roles.predefined_role_service import PredefinedRolesService
from instorage.roles.role import (
    PermissionPublic,
    RoleCreateRequest,
    RolePublic,
    RolesPaginatedResponse,
    RoleUpdateRequest,
)
from instorage.roles.roles_factory import get_roles_service
from instorage.roles.roles_protocol import to_roles_paginated_response
from instorage.roles.roles_service import RolesService
from instorage.server.protocol import responses

router = APIRouter()


@router.get(
    "/permissions/",
    response_model=list[PermissionPublic],
    responses=responses.get_responses([404]),
)
async def get_permissions(service: RolesService = Depends(get_roles_service)):
    return await service.get_permissions()


@router.get(
    "/",
    response_model=RolesPaginatedResponse,
)
async def get_roles(
    service: RolesService = Depends(get_roles_service),
    predefined_roles_service: PredefinedRolesService = Depends(
        get_predefined_roles_service
    ),
):
    roles = await service.get_all_roles()
    predefined_roles = await predefined_roles_service.get_predefined_roles()

    return to_roles_paginated_response(roles=roles, predefined_roles=predefined_roles)


@router.get(
    "/{role_id}/",
    response_model=RolePublic,
    responses=responses.get_responses([404]),
)
async def get_role_by_id(
    role_id: UUID, service: RolesService = Depends(get_roles_service)
):
    return await service.get_role_by_uuid(role_id)


@router.post("/", response_model=RolePublic)
async def create_role(
    role: RoleCreateRequest,
    service: RolesService = Depends(get_roles_service),
):
    return await service.create_role(role)


@router.post(
    "/{role_id}/",
    response_model=RolePublic,
    responses=responses.get_responses([404]),
)
async def update_role(
    role_id: UUID,
    role: RoleUpdateRequest,
    service: RolesService = Depends(get_roles_service),
):
    return await service.update_role(role_id=role_id, role_update=role)


@router.delete(
    "/{role_id}/",
    response_model=RolePublic,
    responses=responses.get_responses([404]),
)
async def delete_role_by_id(
    role_id: UUID, service: RolesService = Depends(get_roles_service)
):
    return await service.delete_role(role_id)
