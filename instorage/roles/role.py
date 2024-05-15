# MIT License

from typing import Optional

from pydantic import BaseModel

from instorage.main.models import InDB, PaginatedResponse, Public
from instorage.predefined_roles.predefined_role import PredefinedRolePublic
from instorage.roles.permissions import Permission


class PermissionPublic(BaseModel):
    name: Permission
    description: str


class RoleBase(BaseModel):
    name: str
    permissions: list[Permission]


class RoleCreateRequest(RoleBase):
    pass


class RoleCreate(RoleCreateRequest):
    tenant_id: int


class RoleUpdateRequest(RoleBase):
    name: Optional[str] = None
    permissions: Optional[list[Permission]] = None


class RoleUpdate(RoleUpdateRequest):
    id: int


class RoleInDB(RoleBase, InDB):
    tenant_id: int


class RolePublic(RoleBase, Public):
    pass


class RolesPaginatedResponse(BaseModel):
    roles: PaginatedResponse[RolePublic]
    predefined_roles: PaginatedResponse[PredefinedRolePublic]
