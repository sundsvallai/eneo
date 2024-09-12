from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import selectinload

from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.assistant_table import AssistantsGroups
from instorage.database.tables.groups_table import Groups
from instorage.database.tables.service_table import ServicesGroups
from instorage.database.tables.users_table import Users
from instorage.groups.group import GroupCreate, GroupInDB, GroupUpdate


class GroupRepository:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session,
            Groups,
            GroupInDB,
            with_options=[
                selectinload(Groups.user).selectinload(Users.roles),
                selectinload(Groups.user).selectinload(Users.predefined_roles),
                selectinload(Groups.embedding_model),
            ],
        )
        self.session = session

    async def get_all_groups(self):
        return await self.delegate.get_all()

    async def get_groups_by_user(self, user_id: UUID) -> list[GroupInDB]:
        query = (
            sa.select(Groups)
            .where(Groups.user_id == user_id)
            .order_by(Groups.created_at)
        )

        return await self.delegate.get_models_from_query(query)

    async def get_group(self, id: UUID) -> GroupInDB:
        return await self.delegate.get(id)

    async def get_groups_by_ids(self, ids: list[UUID]) -> list[GroupInDB]:
        return await self.delegate.get_by_ids(ids)

    async def create_group(self, group: GroupCreate):
        return await self.delegate.add(group)

    async def update_group(self, new_group: GroupUpdate):
        return await self.delegate.update(new_group)

    async def delete_group_by_id(self, id: int) -> GroupInDB:
        return await self.delegate.delete(id)

    async def get_public_groups(self, tenant_id: UUID):
        query = (
            sa.select(Groups)
            .where(Groups.tenant_id == tenant_id)
            .where(Groups.is_public)
            .order_by(Groups.created_at)
        )
        return await self.delegate.get_models_from_query(query)

    async def add_group_to_space(self, group_id: UUID, space_id: UUID):
        query = (
            sa.update(Groups)
            .where(Groups.id == group_id)
            .values(space_id=space_id)
            .returning(Groups)
        )

        return await self.delegate.get_model_from_query(query)

    async def remove_group_from_all_assistants(
        self, group_id: UUID, assistant_ids: list[UUID]
    ):
        stmt = (
            sa.delete(AssistantsGroups)
            .where(AssistantsGroups.group_id == group_id)
            .where(
                AssistantsGroups.assistant_id.not_in(assistant_ids),
            )
        )

        await self.session.execute(stmt)

    async def remove_group_from_all_services(
        self, group_id: UUID, service_ids: list[UUID]
    ):
        stmt = (
            sa.delete(ServicesGroups)
            .where(ServicesGroups.group_id == group_id)
            .where(
                ServicesGroups.service_id.not_in(service_ids),
            )
        )

        await self.session.execute(stmt)
