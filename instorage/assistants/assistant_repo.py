from datetime import datetime
from uuid import UUID

import sqlalchemy as sa

from instorage.assistants.assistant import AssistantInDBWithUser, AssistantUpsert
from instorage.assistants.base.agent_repos import AgentBaseRepository
from instorage.database.database import AsyncSession
from instorage.database.tables.assistant_table import Assistants
from instorage.database.tables.workflow_tables import assistants_steps_guardrails_table


class AssistantRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self._agent_delegate = AgentBaseRepository(
            session, Assistants, AssistantInDBWithUser
        )

    async def add(self, assistant: AssistantUpsert):
        return await self._agent_delegate.add(assistant)

    async def get_by_id(self, id: int):
        return await self._agent_delegate.get_by_id(id)

    async def get_by_uuid(self, uuid: UUID, user_id: int = None):
        return await self._agent_delegate.get_by_uuid(uuid, user_id)

    async def get_by_user(self, user_id: int, search_query: str = None):
        return await self._agent_delegate.get_by_user(user_id, search_query)

    async def get_for_user(self, user_id: int, search_query: str = None):
        return await self._agent_delegate.get_for_user(user_id, search_query)

    async def get_public(self, tenant_id: int, search_query: str = None):
        return await self._agent_delegate.get_public(tenant_id, search_query)

    async def get_for_tenant(
        self,
        tenant_id: int,
        search_query: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
    ):
        return await self._agent_delegate.get_for_tenant(
            tenant_id,
            search_query=search_query,
            start_date=start_date,
            end_date=end_date,
        )

    async def update(self, assistant: AssistantUpsert):
        return await self._agent_delegate.update(assistant)

    async def delete(self, uuid: UUID, user_id: int):
        return await self._agent_delegate.delete(uuid, user_id)

    async def add_guard(self, guard_step_id: int, assistant_id: int):
        stmt = sa.insert(assistants_steps_guardrails_table).values(
            assistant_id=assistant_id, step_id=guard_step_id
        )

        await self.session.execute(stmt)
