from typing import TYPE_CHECKING

from intric.main.exceptions import NotFoundException

if TYPE_CHECKING:
    from uuid import UUID

    from intric.templates.app_template.api.app_template_models import AppTemplateCreate
    from intric.templates.app_template.app_template import AppTemplate
    from intric.templates.app_template.app_template_factory import (
        AppTemplateFactory,
    )
    from intric.templates.app_template.app_template_repo import (
        AppTemplateRepository,
    )
    from intric.templates.app_template.api.app_template_models import AppTemplateUpdate


class AppTemplateService:
    def __init__(
        self,
        factory: "AppTemplateFactory",
        repo: "AppTemplateRepository",
    ) -> None:
        self.factory = factory
        self.repo = repo

    async def get_app_template(self, app_template_id: "UUID") -> "AppTemplate":
        app_template = await self.repo.get_by_id(app_template_id=app_template_id)

        if app_template is None:
            raise NotFoundException()

        return app_template

    async def get_app_templates(self) -> list["AppTemplate"]:
        return await self.repo.get_app_template_list()

    async def create_app_template(self, obj: "AppTemplateCreate") -> "AppTemplate":
        template = await self.repo.add(obj=obj)
        return template

    async def delete_app_template(self, id: "UUID") -> None:
        await self.repo.delete(id=id)

    async def update_app_template(
        self,
        id: "UUID",
        obj: "AppTemplateUpdate",
    ) -> "AppTemplate":
        return await self.repo.update(id=id, obj=obj)
