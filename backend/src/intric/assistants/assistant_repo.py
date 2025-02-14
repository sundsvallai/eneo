from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import selectinload

from intric.assistants.assistant import Assistant
from intric.assistants.assistant_factory import AssistantFactory
from intric.database.database import AsyncSession
from intric.database.tables.assistant_table import (
    Assistants,
    AssistantsFiles,
    AssistantsGroups,
    AssistantsWebsites,
)
from intric.database.tables.groups_table import Groups
from intric.database.tables.info_blobs_table import InfoBlobs
from intric.database.tables.prompts_table import Prompts, PromptsAssistants
from intric.database.tables.users_table import Users
from intric.database.tables.websites_table import CrawlRuns, Websites
from intric.database.tables.workflow_tables import assistants_steps_guardrails_table
from intric.files.file_models import FileInfo
from intric.groups.api.group_models import Group
from intric.prompts.prompt import Prompt
from intric.websites.website_models import WebsiteSparse


class AssistantRepository:
    def __init__(
        self,
        session: AsyncSession,
        factory: AssistantFactory,
    ):
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
            selectinload(Assistants.attachments).selectinload(AssistantsFiles.file),
            selectinload(Assistants.template),
        ]

    async def _set_is_selected_to_false(self, assistant_id: UUID):
        stmt = (
            sa.update(PromptsAssistants)
            .values(is_selected=False)
            .where(PromptsAssistants.assistant_id == assistant_id)
        )

        await self.session.execute(stmt)

    async def _add_assistant_prompt_entry(self, assistant_id: UUID, prompt_id: UUID):
        stmt = (
            sa.insert(PromptsAssistants)
            .values(assistant_id=assistant_id, prompt_id=prompt_id, is_selected=True)
            .returning(PromptsAssistants)
        )

        return await self.session.scalar(stmt)

    async def _get_assistant_prompt_entry(self, assistant_id: UUID, prompt_id: UUID):
        stmt = (
            sa.select(PromptsAssistants)
            .where(PromptsAssistants.prompt_id == prompt_id)
            .where(PromptsAssistants.assistant_id == assistant_id)
        )

        return await self.session.scalar(stmt)

    async def _select_assistant_prompt_entry(self, assistant_id: UUID, prompt_id: UUID):
        stmt = (
            sa.update(PromptsAssistants)
            .where(PromptsAssistants.prompt_id == prompt_id)
            .where(PromptsAssistants.assistant_id == assistant_id)
            .values(is_selected=True)
        )

        await self.session.execute(stmt)

    async def _add_prompt(self, assistant_id: UUID, prompt: Prompt):
        await self._set_is_selected_to_false(assistant_id=assistant_id)

        prompt_assistant_entry = await self._get_assistant_prompt_entry(
            assistant_id=assistant_id, prompt_id=prompt.id
        )

        if prompt_assistant_entry is not None:
            await self._select_assistant_prompt_entry(
                assistant_id=assistant_id, prompt_id=prompt.id
            )
        else:
            await self._add_assistant_prompt_entry(
                assistant_id=assistant_id, prompt_id=prompt.id
            )

        return prompt

    async def _get_selected_prompt(self, assistant_id: UUID):
        stmt = (
            sa.select(Prompts)
            .join(PromptsAssistants)
            .where(PromptsAssistants.prompt_id == Prompts.id)
            .where(PromptsAssistants.assistant_id == assistant_id)
            .where(PromptsAssistants.is_selected)
            .options(selectinload(Prompts.user))
        )

        return await self.session.scalar(stmt)

    async def _set_attachments(
        self, assistant_in_db: Assistants, attachments: list[FileInfo]
    ):
        # Delete all
        stmt = sa.delete(AssistantsFiles).where(
            AssistantsFiles.assistant_id == assistant_in_db.id
        )
        await self.session.execute(stmt)

        # Add attachments
        if attachments:
            attachments_dicts = [
                dict(assistant_id=assistant_in_db.id, file_id=file.id)
                for file in attachments
            ]

            stmt = sa.insert(AssistantsFiles).values(attachments_dicts)
            await self.session.execute(stmt)

        await self.session.refresh(assistant_in_db)

    async def _set_groups(self, assistant_in_db: Assistants, groups: list[Group]):
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
        prompt = await self._get_selected_prompt(entry_in_db.id)

        return self.factory.create_assistant_from_db(
            entry_in_db, groups_in_db=groups, prompt=prompt
        )

    async def get_record_with_options(self, query):
        for option in self._options():
            query = query.options(option)

        return await self.session.scalar(query)

    async def get_records_with_options(self, query):
        for option in self._options():
            query = query.options(option)

        return await self.session.scalars(query)

    async def add(self, assistant: Assistant):
        completion_model_id = (
            assistant.completion_model.id
            if assistant.completion_model is not None
            else None
        )

        template_id = (
            assistant.source_template.id if assistant.source_template else None
        )
        query = (
            sa.insert(Assistants)
            .values(
                name=assistant.name,
                user_id=assistant.user.id,
                completion_model_id=completion_model_id,
                completion_model_kwargs=assistant.completion_model_kwargs.model_dump(),
                logging_enabled=assistant.logging_enabled,
                guardrail_active=False,
                space_id=assistant.space_id,
                is_default=assistant.is_default,
                published=assistant.published,
                template_id=template_id,
            )
            .returning(Assistants)
        )
        entry_in_db = await self.get_record_with_options(query)

        # Assign groups and websites
        await self._set_groups(entry_in_db, assistant.groups)
        await self._set_websites(entry_in_db, assistant.websites)
        await self._set_attachments(entry_in_db, attachments=assistant.attachments)

        if assistant.prompt:
            await self._add_prompt(assistant_id=entry_in_db.id, prompt=assistant.prompt)

        prompt = await self._get_selected_prompt(entry_in_db.id)

        return self.factory.create_assistant_from_db(entry_in_db, prompt=prompt)

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
                completion_model_id=assistant.completion_model.id,
                completion_model_kwargs=assistant.completion_model_kwargs.model_dump(),
                logging_enabled=assistant.logging_enabled,
                space_id=assistant.space_id,
                published=assistant.published,
            )
            .where(Assistants.id == assistant.id)
            .returning(Assistants)
        )
        entry_in_db = await self.get_record_with_options(query)

        # assign groups and websites
        await self._set_groups(entry_in_db, assistant.groups)
        await self._set_websites(entry_in_db, assistant.websites)
        await self._set_attachments(entry_in_db, assistant.attachments)

        if assistant.prompt:
            await self._add_prompt(assistant_id=entry_in_db.id, prompt=assistant.prompt)

        groups = await self._get_groups(assistant.id)
        prompt = await self._get_selected_prompt(assistant.id)

        return self.factory.create_assistant_from_db(
            entry_in_db, groups_in_db=groups, prompt=prompt
        )

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

    async def get_by_space(self, space_id: UUID):
        query = (
            sa.select(Assistants)
            .where(Assistants.space_id == space_id)
            .order_by(Assistants.created_at)
        )

        records = await self.get_records_with_options(query)

        assistants = []
        for record in records:
            groups = await self._get_groups(record.id)
            prompt = await self._get_selected_prompt(record.id)
            assistant = self.factory.create_assistant_from_db(
                record, prompt=prompt, groups_in_db=groups
            )
            assistants.append(assistant)

        return assistants
