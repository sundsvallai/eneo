# MIT License

from typing import List
from uuid import UUID

from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.roles_table import PredefinedRoles
from instorage.predefined_roles.predefined_role import (
    PredefinedRoleCreate,
    PredefinedRoleInDB,
    PredefinedRoleUpdate,
)


class PredefinedRolesRepository:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session, PredefinedRoles, PredefinedRoleInDB
        )

    async def get_predefined_role_by_uuid(self, id: UUID) -> PredefinedRoleInDB:
        return await self.delegate.get(id)

    async def get_predefined_role_by_name(self, name: str) -> PredefinedRoleInDB:
        return await self.delegate.get_by(conditions={PredefinedRoles.name: name})

    async def create_predefined_role(
        self, role: PredefinedRoleCreate
    ) -> PredefinedRoleInDB:
        return await self.delegate.add(role)

    async def update_predefined_role(
        self, role: PredefinedRoleUpdate
    ) -> PredefinedRoleInDB:
        return await self.delegate.update(role)

    async def delete_predefined_role_by_id(self, id: UUID) -> PredefinedRoleInDB:
        return await self.delegate.delete(id)

    async def get_predefined_roles(self) -> List[PredefinedRoleInDB]:
        return await self.delegate.get_all()
