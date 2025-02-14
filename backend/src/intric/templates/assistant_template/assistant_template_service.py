from typing import TYPE_CHECKING

from intric.main.exceptions import NotFoundException
from intric.templates.assistant_template.api.assistant_template_models import (
    AssistantTemplateCreate,
)

if TYPE_CHECKING:
    from uuid import UUID

    from intric.templates.assistant_template.assistant_template import AssistantTemplate
    from intric.templates.assistant_template.assistant_template_factory import (
        AssistantTemplateFactory,
    )
    from intric.templates.assistant_template.assistant_template_repo import (
        AssistantTemplateRepository,
    )
    from intric.templates.assistant_template.api.assistant_template_models import (
        AssistantTemplateUpdate,
    )


class AssistantTemplateService:
    def __init__(
        self,
        factory: "AssistantTemplateFactory",
        repo: "AssistantTemplateRepository",
    ) -> None:
        self.factory = factory
        self.repo = repo

    async def get_assistant_template(
        self, assistant_template_id: "UUID"
    ) -> "AssistantTemplate":
        assistant_template = await self.repo.get_by_id(
            assistant_template_id=assistant_template_id
        )

        if assistant_template is None:
            raise NotFoundException()

        return assistant_template

    async def get_assistant_templates(self) -> list["AssistantTemplate"]:
        return await self.repo.get_assistant_template_list()

    async def create_assistant_template(
        self, obj: AssistantTemplateCreate
    ) -> "AssistantTemplate":
        template = await self.repo.add(obj=obj)
        return template

    async def delete_assistant_template(self, id: "UUID") -> None:
        await self.repo.delete(id=id)

    async def update_assistant_template(
        self,
        id: "UUID",
        obj: "AssistantTemplateUpdate",
    ) -> "AssistantTemplate":
        return await self.repo.update(id=id, obj=obj)
