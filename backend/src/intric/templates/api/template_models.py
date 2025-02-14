from pydantic import BaseModel, computed_field

from intric.templates.app_template.api.app_template_models import AppTemplatePublic
from intric.templates.assistant_template.api.assistant_template_models import (
    AssistantTemplatePublic,
)


class TemplateListPublic(BaseModel):
    items: list[AppTemplatePublic | AssistantTemplatePublic]

    @computed_field
    def count(self) -> int:
        return len(self.items)
