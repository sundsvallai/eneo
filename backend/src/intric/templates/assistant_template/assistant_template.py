from typing import TYPE_CHECKING

from intric.main.exceptions import BadRequestException
from intric.spaces.api.space_models import WizardType


if TYPE_CHECKING:
    from datetime import datetime
    from uuid import UUID

    from intric.ai_models.completion_models.completion_model import (
        CompletionModelPublic,
    )
    from intric.spaces.api.space_models import TemplateCreate

    from intric.templates.assistant_template.api.assistant_template_models import (
        AssistantTemplateWizard,
    )


class AssistantTemplate:
    def __init__(
        self,
        id: "UUID",
        name: str,
        description: str,
        category: str,
        prompt_text: str,
        created_at: "datetime",
        updated_at: "datetime",
        completion_model: "CompletionModelPublic",
        completion_model_kwargs: dict,
        wizard: "AssistantTemplateWizard",
        organization: str,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.prompt_text = prompt_text
        self.completion_model_kwargs = completion_model_kwargs
        self.wizard = wizard
        self.completion_model = completion_model
        self.created_at = created_at
        self.updated_at = updated_at
        self.organization = organization

    def validate_assistant_wizard_data(self, template_data: "TemplateCreate") -> None:
        for data in template_data.additional_fields:
            if data.type == WizardType.attachments:
                if (
                    self.wizard.attachments is None
                    or self.wizard.attachments.required is False
                ):
                    raise BadRequestException(
                        "Unexpected attachments data when creating assistant"
                    )
            elif data.type == WizardType.groups:
                if (
                    self.wizard.collections is None
                    or self.wizard.collections.required is False
                ):
                    raise BadRequestException(
                        "Unexpected groups data when creating assistant"
                    )
            else:
                raise BadRequestException("Unsupported type")

    def is_from_intric(self) -> bool:
        return self.organization == 'default'
