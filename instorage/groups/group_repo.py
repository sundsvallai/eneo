from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import selectinload

from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.groups_table import Groups
from instorage.database.tables.user_groups_table import UserGroups
from instorage.database.tables.users_table import Users
from instorage.groups.group import GroupCreate, GroupInDB, GroupUpdate


class GroupRepository:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session,
            Groups,
            GroupInDB,
            with_options=[
                selectinload(Groups.user_groups),
                selectinload(Groups.user).selectinload(Users.roles),
                selectinload(Groups.user).selectinload(Users.predefined_roles),
            ],
        )

    async def get_all_groups(self):
        return await self.delegate.get_all()

    async def get_all_groups_from_user_group(self, user_id: int):
        query = (
            sa.select(Groups)
            .outerjoin(UserGroups, Groups.user_groups)
            .outerjoin(Users, UserGroups.users)
            .where((Groups.user_id == user_id) | (Users.id == user_id))
            .order_by(Groups.created_at)
        )
        return await self.delegate.get_models_from_query(query=query)

    async def get_group_by_id(self, id: int):
        return await self.delegate.get(id)

    async def get_group_by_uuid(self, uuid: UUID) -> GroupInDB:
        return await self.delegate.get_by(conditions={Groups.uuid: uuid})

    async def create_group(self, group: GroupCreate):
        return await self.delegate.add(group)

    async def update_group(self, new_group: GroupUpdate):
        return await self.delegate.update(new_group)

    async def delete_group_by_id(self, id: int) -> GroupInDB:
        return await self.delegate.delete(id)

    async def get_public_groups(self, tenant_id: int):
        query = (
            sa.select(Groups)
            .where(Groups.tenant_id == tenant_id)
            .where(Groups.is_public)
            .order_by(Groups.created_at)
        )
        return await self.delegate.get_models_from_query(query)
