# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

from uuid import UUID

from instorage.main.exceptions import NotFoundException
from instorage.predefined_roles.predefined_role import PredefinedRoleInDB
from instorage.predefined_roles.predefined_roles_repo import PredefinedRolesRepository


class PredefinedRolesService:
    def __init__(self, repo: PredefinedRolesRepository):
        self.repo = repo

    def _validate(self, role: PredefinedRoleInDB, role_id: UUID):
        if role is None:
            raise NotFoundException(f"PredefinedRole {role_id} not found")

    async def get_predefined_role(self, role_id: UUID) -> PredefinedRoleInDB:
        role = await self.repo.get_predefined_role_by_uuid(role_id)
        self._validate(role, role_id)

        return role

    async def get_predefined_roles(self):
        return await self.repo.get_predefined_roles()
