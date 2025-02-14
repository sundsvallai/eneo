from typing import TYPE_CHECKING

from intric.main.exceptions import BadRequestException
from intric.spaces.api.space_models import WizardType


if TYPE_CHECKING:
    from uuid import UUID
    from datetime import datetime
    from intric.ai_models.completion_models.completion_model import (
        CompletionModelPublic,
    )

    from intric.spaces.api.space_models import TemplateCreate
    from intric.templates.app_template.api.app_template_models import AppTemplateWizard


class AppTemplate:
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
        wizard: "AppTemplateWizard",
        input_description: str | None,
        input_type: str,
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
        self.input_description = input_description
        self.input_type = input_type
        self.organization = organization

    def validate_wizard_data(self, template_data: "TemplateCreate") -> None:
        for data in template_data.additional_fields:
            # App only supports attachment atm
            if data.type != WizardType.attachments:
                raise BadRequestException("Unsupported type")

            if (
                self.wizard.attachments is None
                or self.wizard.attachments.required is False
            ):
                raise BadRequestException(
                    "Unexpected attachments data when creating assistant"
                )

    def is_from_intric(self) -> bool:
        return self.organization == 'default'
