from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import selectinload

from instorage.assistants.assistant import Assistant
from instorage.assistants.assistant_factory import AssistantFactory
from instorage.database.database import AsyncSession
from instorage.database.tables.assistant_table import (
    Assistants,
    AssistantsGroups,
    AssistantsWebsites,
)
from instorage.database.tables.groups_table import Groups
from instorage.database.tables.info_blobs_table import InfoBlobs
from instorage.database.tables.users_table import Users
from instorage.database.tables.websites_table import CrawlRuns, Websites
from instorage.database.tables.workflow_tables import assistants_steps_guardrails_table
from instorage.groups.group import GroupSparse
from instorage.websites.website_models import WebsiteSparse


class AssistantRepository:
    def __init__(self, session: AsyncSession, factory: AssistantFactory):
        self.session = session
        self.factory = factory

    @staticmethod
    def _options():
        return [
            selectinload(Assistants.completion_model),
            selectinload(Assistants.user).selectinload(Users.tenant),
            selectinload(Assistants.user).selectinload(Users.roles),
            selectinload(Assistants.user).selectinload(Users.predefined_roles),
            selectinload(Assistants.websites)
            .selectinload(Websites.latest_crawl)
            .selectinload(CrawlRuns.job),
            selectinload(Assistants.websites).selectinload(Websites.embedding_model),
        ]

    async def _set_groups(self, assistant_in_db: Assistants, groups: list[GroupSparse]):
        # Delete all
        stmt = sa.delete(AssistantsGroups).where(
            AssistantsGroups.assistant_id == assistant_in_db.id
        )
        await self.session.execute(stmt)

        if groups:
            stmt = sa.insert(AssistantsGroups).values(
                [
                    dict(group_id=group.id, assistant_id=assistant_in_db.id)
                    for group in groups
                ]
            )
            await self.session.execute(stmt)

        await self.session.refresh(assistant_in_db)

    async def _set_websites(
        self, assistant_in_db: Assistants, websites: list[WebsiteSparse]
    ):
        # Delete all
        stmt = sa.delete(AssistantsWebsites).where(
            AssistantsWebsites.assistant_id == assistant_in_db.id
        )
        await self.session.execute(stmt)

        if websites:
            stmt = sa.insert(AssistantsWebsites).values(
                [
                    dict(website_id=website.id, assistant_id=assistant_in_db.id)
                    for website in websites
                ]
            )
            await self.session.execute(stmt)

        await self.session.refresh(assistant_in_db)

    async def _get_groups(self, assistant_id: UUID):
        query = (
            sa.select(
                Groups,
                sa.func.coalesce(sa.func.count(InfoBlobs.id).label("infoblob_count")),
            )
            .outerjoin(InfoBlobs, Groups.id == InfoBlobs.group_id)
            .outerjoin(AssistantsGroups, AssistantsGroups.group_id == Groups.id)
            .where(AssistantsGroups.assistant_id == assistant_id)
            .group_by(Groups.id)
            .order_by(Groups.created_at)
            .options(selectinload(Groups.embedding_model))
        )

        res = await self.session.execute(query)
        return res.all()

    async def _get_from_query(self, query: sa.Select):
        entry_in_db = await self.get_record_with_options(query)

        if not entry_in_db:
            return

        groups = await self._get_groups(entry_in_db.id)

        return self.factory.create_assistant_from_db(entry_in_db, groups_in_db=groups)

    async def get_record_with_options(self, query):
        for option in self._options():
            query = query.options(option)

        return await self.session.scalar(query)

    async def get_records_with_options(self, query):
        for option in self._options():
            query = query.options(option)

        return await self.session.scalars(query)

    async def add(self, assistant: Assistant):
        query = (
            sa.insert(Assistants)
            .values(
                name=assistant.name,
                prompt=assistant.prompt,
                user_id=assistant.user.id,
                completion_model_id=assistant.completion_model.id,
                completion_model_kwargs=assistant.completion_model_kwargs.model_dump(),
                logging_enabled=assistant.logging_enabled,
                guardrail_active=False,
                space_id=assistant.space_id,
            )
            .returning(Assistants)
        )
        entry_in_db = await self.get_record_with_options(query)

        # assign groups and websites
        await self._set_groups(entry_in_db, assistant.groups)
        await self._set_websites(entry_in_db, assistant.websites)

        return self.factory.create_assistant_from_db(entry_in_db)

    async def get_by_id(self, id: UUID):
        query = sa.select(Assistants).where(Assistants.id == id)
        return await self._get_from_query(query)

    async def get_for_user(self, user_id: UUID, search_query: str = None):
        query = (
            sa.select(Assistants)
            .where(Assistants.user_id == user_id)
            .order_by(Assistants.created_at)
        )

        if search_query is not None:
            query = query.filter(Assistants.name.like(f"%{search_query}%"))

        records = await self.get_records_with_options(query)

        return [self.factory.create_assistant_from_db(record) for record in records]

    async def get_for_tenant(
        self,
        tenant_id: UUID,
        search_query: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
    ):
        query = (
            sa.select(Assistants)
            .join(Users)
            .where(Users.tenant_id == tenant_id)
            .order_by(Assistants.created_at)
        )

        if start_date is not None:
            query = query.filter(Assistants.created_at >= start_date)

        if end_date is not None:
            query = query.filter(Assistants.created_at <= end_date)

        if search_query is not None:
            query = query.filter(Assistants.name.like(f"%{search_query}%"))

        records = await self.get_records_with_options(query)

        return [self.factory.create_assistant_from_db(record) for record in records]

    async def update(self, assistant: Assistant):
        query = (
            sa.update(Assistants)
            .values(
                name=assistant.name,
                prompt=assistant.prompt,
                completion_model_id=assistant.completion_model.id,
                completion_model_kwargs=assistant.completion_model_kwargs.model_dump(),
                logging_enabled=assistant.logging_enabled,
                space_id=assistant.space_id,
            )
            .where(Assistants.id == assistant.id)
            .returning(Assistants)
        )
        entry_in_db = await self.get_record_with_options(query)

        # assign groups and websites
        await self._set_groups(entry_in_db, assistant.groups)
        await self._set_websites(entry_in_db, assistant.websites)

        groups = await self._get_groups(assistant.id)

        return self.factory.create_assistant_from_db(entry_in_db, groups_in_db=groups)

    async def delete(self, id: UUID):
        query = sa.delete(Assistants).where(Assistants.id == id)
        await self.session.execute(query)

    async def add_guard(self, guard_step_id: UUID, assistant_id: UUID):
        stmt = sa.insert(assistants_steps_guardrails_table).values(
            assistant_id=assistant_id, step_id=guard_step_id
        )

        await self.session.execute(stmt)

    async def add_assistant_to_space(self, assistant_id: UUID, space_id: UUID):
        query = (
            sa.update(Assistants)
            .where(Assistants.id == assistant_id)
            .values(space_id=space_id)
            .returning(Assistants)
        )

        return await self._get_from_query(query)
