from typing import TYPE_CHECKING, Optional

import sqlalchemy as sa
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from intric.database.tables.assistant_template_table import AssistantTemplates

if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy import Select
    from sqlalchemy.ext.asyncio import AsyncSession

    from intric.templates.assistant_template.api.assistant_template_models import (
        AssistantTemplateCreate,
        AssistantTemplateUpdate,
    )
    from intric.templates.assistant_template.assistant_template import AssistantTemplate
    from intric.templates.assistant_template.assistant_template_factory import (
        AssistantTemplateFactory,
    )


class AssistantTemplateRepository:
    def __init__(self, session: "AsyncSession", factory: "AssistantTemplateFactory"):
        self.session = session
        self.factory = factory

        self._db_model = AssistantTemplates
        # db relations
        self._options = [selectinload(self._db_model.completion_model)]

    def _apply_options(self, query: "Select") -> "Select":
        for option in self._options:
            query = query.options(option)

        return query

    async def get_by_id(
        self, assistant_template_id: "UUID"
    ) -> Optional["AssistantTemplate"]:
        base_query = select(self._db_model).where(
            self._db_model.id == assistant_template_id
        )
        query = self._apply_options(query=base_query)

        record = await self.session.scalar(query)

        if not record:
            return None

        return self.factory.create_assistant_template(item=record)

    async def get_assistant_template_list(self) -> list["AssistantTemplate"]:
        base_query = select(self._db_model)
        query = self._apply_options(query=base_query)

        results = await self.session.scalars(query)

        return self.factory.create_assistant_template_list(items=results.all())

    async def add(self, obj: "AssistantTemplateCreate") -> "AssistantTemplate":
        stmt = (
            sa.insert(AssistantTemplates)
            .values(
                name=obj.name,
                description=obj.description,
                category=obj.category,
                prompt_text=obj.prompt,
                wizard=obj.wizard.model_dump(),
                completion_model_kwargs=obj.completion_model_kwargs,
            )
            .returning(AssistantTemplates)
        )
        result = await self.session.execute(stmt)
        template = result.scalar_one()

        return self.factory.create_assistant_template(item=template)

    async def delete(self, id: "UUID") -> None:
        stmt = sa.delete(self._db_model).where(self._db_model.id == id)
        await self.session.execute(stmt)

    async def update(
        self,
        id: "UUID",
        obj: "AssistantTemplateUpdate",
    ) -> "AssistantTemplate":
        stmt = (
            sa.update(self._db_model)
            .values(
                name=obj.name,
                description=obj.description,
                category=obj.category,
                prompt_text=obj.prompt,
                organization=obj.organization,
                wizard=obj.wizard.model_dump(),
            )
            .where(self._db_model.id == id)
            .returning(self._db_model)
        )
        result = await self.session.execute(stmt)
        template_updated = result.scalar_one()
        return self.factory.create_assistant_template(item=template_updated)
