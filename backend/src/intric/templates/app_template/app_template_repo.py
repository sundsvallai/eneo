from typing import TYPE_CHECKING, Optional

import sqlalchemy as sa
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from intric.database.tables.app_template_table import AppTemplates

if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncSession

    from intric.templates.app_template.api.app_template_models import (
        AppTemplateCreate,
        AppTemplateUpdate,
    )
    from intric.templates.app_template.app_template import AppTemplate
    from intric.templates.app_template.app_template_factory import (
        AppTemplateFactory,
    )


class AppTemplateRepository:
    def __init__(self, session: "AsyncSession", factory: "AppTemplateFactory"):
        self.session = session
        self.factory = factory

        self._db_model = AppTemplates
        # db relations
        self._options = [selectinload(self._db_model.completion_model)]

    async def get_by_id(self, app_template_id) -> Optional["AppTemplate"]:
        query = (
            select(self._db_model)
            .options(*self._options)
            .where(self._db_model.id == app_template_id)
        )

        record = await self.session.scalar(query)

        if not record:
            return None

        return self.factory.create_app_template(item=record)

    async def get_app_template_list(self) -> list["AppTemplate"]:
        query = select(self._db_model).options(*self._options)
        results = await self.session.scalars(query)

        return self.factory.create_app_template_list(items=results.all())

    async def add(self, obj: "AppTemplateCreate") -> "AppTemplate":
        stmt = (
            sa.insert(self._db_model)
            .values(
                name=obj.name,
                description=obj.description,
                category=obj.category,
                prompt_text=obj.prompt,
                wizard=obj.wizard.model_dump(),
                completion_model_kwargs=obj.completion_model_kwargs,
                input_type=obj.input_type,
                input_description=obj.input_description,
            )
            .returning(self._db_model)
        )
        result = await self.session.execute(stmt)
        template = result.scalar_one()

        return self.factory.create_app_template(item=template)

    async def delete(self, id: "UUID") -> None:
        stmt = sa.delete(self._db_model).where(self._db_model.id == id)
        await self.session.execute(stmt)

    async def update(
        self,
        id: "UUID",
        obj: "AppTemplateUpdate",
    ) -> "AppTemplate":
        stmt = (
            sa.update(self._db_model)
            .values(
                name=obj.name,
                description=obj.description,
                category=obj.category,
                prompt_text=obj.prompt,
                organization=obj.organization,
                wizard=obj.wizard.model_dump(),
                input_type=obj.input_type,
                input_description=obj.input_description,
            )
            .where(self._db_model.id == id)
            .returning(self._db_model)
        )
        result = await self.session.execute(stmt)
        template_updated = result.scalar_one()
        return self.factory.create_app_template(item=template_updated)
