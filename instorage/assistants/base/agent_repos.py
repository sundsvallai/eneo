from datetime import datetime
from typing import Type
from uuid import UUID

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy.orm import selectinload

from instorage.assistants.assistant import AssistantInDBWithUser, AssistantUpsert
from instorage.database.database import AsyncSession
from instorage.database.repositories.base import (
    BaseRepositoryDelegate,
    RelationshipOption,
)
from instorage.database.tables.assistant_table import Assistants
from instorage.database.tables.groups_table import Groups
from instorage.database.tables.service_table import Services
from instorage.database.tables.user_groups_table import UserGroups
from instorage.database.tables.users_table import Users
from instorage.database.tables.workflow_tables import Steps
from instorage.services.service import ServiceInDBWithUser, ServiceUpsert


class AgentBaseRepository:
    def __init__(
        self,
        session: AsyncSession,
        table: Type[Assistants | Services],
        in_db_model: Type[AssistantInDBWithUser | ServiceInDBWithUser],
    ):
        self.delegate = BaseRepositoryDelegate(
            session,
            table,
            in_db_model,
            with_options=self._get_options(),
        )
        self.table = table

    def _get_options(self):
        return [
            selectinload(Assistants.groups),
            selectinload(Assistants.user).selectinload(Users.tenant),
            selectinload(Assistants.user).selectinload(Users.roles),
            selectinload(Assistants.user).selectinload(Users.predefined_roles),
            selectinload(Assistants.guard_step)
            .selectinload(Steps.service)
            .selectinload(Services.groups),
            selectinload(Assistants.guard_step).selectinload(Steps.filter),
            selectinload(Assistants.guard_step)
            .selectinload(Steps.service)
            .selectinload(Services.groups),
            selectinload(Assistants.guard_step)
            .selectinload(Steps.service)
            .selectinload(Services.user_groups),
            selectinload(Assistants.user_groups),
            selectinload(Services.user_groups),
        ]

    async def _get_assistants(self, stmt: sa.Select, search_query: str = None):
        stmt = stmt.where(self.table.type == self._get_current_table_type())

        if search_query is not None:
            stmt = stmt.filter(self.table.name.like(f"%{search_query}%"))

        return await self.delegate.get_models_from_query(stmt)

    def _get_table_type(self, table: Type[Assistants | Services]):
        return table.__mapper_args__["polymorphic_identity"]

    def _get_current_table_type(self):
        return self._get_table_type(self.table)

    @staticmethod
    def _get_relationship_options():
        return [
            RelationshipOption(
                name="groups",
                table=Groups,
            ),
        ]

    async def add(self, upsert_entry: AssistantUpsert | ServiceUpsert):
        return await self.delegate.add(
            upsert_entry,
            exclude={"guardrail"},
            relationships=self._get_relationship_options(),
            type=self._get_current_table_type(),
        )

    async def update(self, new_entry: BaseModel):
        return await self.delegate.update(
            new_entry,
            exclude={"guardrail"},
            relationships=self._get_relationship_options(),
        )

    async def get_by_id(self, id: int):
        return await self.delegate.get(id)

    async def get_by_uuid(self, uuid: UUID, user_id: int = None):
        conditions = {self.table.uuid: uuid}

        if user_id is not None:
            conditions[self.table.user_id] = user_id

        return await self.delegate.get_by(conditions=conditions)

    async def get_by_user(self, user_id: int, search_query: str = None):
        query = (
            sa.select(self.table)
            .where(self.table.user_id == user_id)
            .order_by(self.table.created_at)
        )

        return await self._get_assistants(query, search_query)

    async def get_for_user(self, user_id: int, search_query: str = None):
        query = (
            sa.select(self.table)
            .outerjoin(UserGroups, self.table.user_groups)
            .outerjoin(Users, UserGroups.users)
            .where((self.table.user_id == user_id) | (Users.id == user_id))
            .order_by(self.table.created_at)
        )

        return await self._get_assistants(query, search_query)

    async def get_public(self, tenant_id: int, search_query: str = None):
        query = (
            sa.select(self.table)
            .join(Users)
            .where(Users.tenant_id == tenant_id)
            .where(self.table.is_public)
            .order_by(self.table.created_at)
        )

        return await self._get_assistants(query, search_query)

    async def get_for_tenant(
        self,
        tenant_id: int,
        search_query: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
    ):
        query = (
            sa.select(self.table)
            .join(Users)
            .where(Users.tenant_id == tenant_id)
            .order_by(self.table.created_at)
        )

        if start_date is not None:
            query = query.filter(self.table.created_at >= start_date)

        if end_date is not None:
            query = query.filter(self.table.created_at <= end_date)

        return await self._get_assistants(query, search_query)

    async def delete(self, uuid: UUID, user_id: int):
        return await self.delegate.delete_by(
            conditions={self.table.uuid: uuid, self.table.user_id: user_id}
        )
