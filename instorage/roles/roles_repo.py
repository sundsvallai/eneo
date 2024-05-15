# MIT License

from typing import List
from uuid import UUID

from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.roles_table import Roles
from instorage.roles.role import RoleCreate, RoleInDB, RoleUpdate


class RolesRepository:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(session, Roles, RoleInDB)
        self.session = session

    async def get_role_by_uuid(self, uuid: UUID) -> RoleInDB:
        return await self.delegate.get_by(conditions={Roles.uuid: uuid})

    async def create_role(self, role: RoleCreate) -> RoleInDB:
        return await self.delegate.add(role)

    async def update_role(self, role: RoleUpdate) -> RoleInDB:
        return await self.delegate.update(role)

    async def delete_role_by_id(self, uuid: UUID) -> RoleInDB:
        return await self.delegate.delete_by_uuid(uuid)

    async def get_by_tenant(self, tenant_id: int) -> List[RoleInDB]:
        return await self.delegate.filter_by(conditions={Roles.tenant_id: tenant_id})
