from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, computed_field, model_validator

from intric.apps.apps.api.app_models import InputFieldType


class TemplateWizard(BaseModel):
    required: bool = False
    title: Optional[str] = None
    description: Optional[str] = None


class AppTemplateWizard(BaseModel):
    attachments: Optional[TemplateWizard]
    collections: Optional[TemplateWizard]

    @model_validator(mode="after")
    def validate_collections(self):
        # No collections are allowed for App
        if self.collections is not None:
            raise ValueError("The 'collections' field must always be None.")
        return self


class CompletionModelPublicAppTemplate(BaseModel):
    id: UUID


class PromptPublicAppTemplate(BaseModel):
    text: Optional[str]


class AppTemplateOrganization(BaseModel):
    name: str


class AppInTemplatePublic(BaseModel):
    name: str
    completion_model: Optional[CompletionModelPublicAppTemplate]
    completion_model_kwargs: dict
    prompt: Optional[PromptPublicAppTemplate]
    input_description: Optional[str]
    input_type: str


class AppTemplatePublic(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    name: str
    description: Optional[str]
    category: str
    app: AppInTemplatePublic
    type: Literal["app"]
    wizard: AppTemplateWizard
    organization: AppTemplateOrganization


class AppTemplateListPublic(BaseModel):
    items: list[AppTemplatePublic]

    @computed_field(description="Number of items returned in the response")
    @property
    def count(self) -> int:
        return len(self.items)


class AppTemplateCreate(BaseModel):
    name: str
    description: str
    category: str
    prompt: str
    organization: Optional[str] = None
    completion_model_kwargs: Optional[dict] = {}
    wizard: AppTemplateWizard
    input_type: str
    input_description: Optional[str]

    @model_validator(mode="after")
    def validate_input_type(self):
        if not InputFieldType.contains_input_type(self.input_type):
            raise ValueError("Not a valid input type for App")
        return self


class AppTemplateUpdate(AppTemplateCreate):
    pass
