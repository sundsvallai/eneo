from enum import Enum

from pydantic import BaseModel, ConfigDict

from intric.ai_models.completion_models.completion_model import (
    CompletionModelSparse,
    ModelKwargs,
)
from intric.files.file_models import FilePublic, FileRestrictions
from intric.main.models import InDB, ModelId, ResourcePermissionsMixin, partial_model
from intric.prompts.api.prompt_models import PromptCreate, PromptPublic


class InputFieldType(str, Enum):
    TEXT_FIELD = "text-field"
    TEXT_UPLOAD = "text-upload"
    AUDIO_UPLOAD = "audio-upload"
    AUDIO_RECORDER = "audio-recorder"
    IMAGE_UPLOAD = "image-upload"

    @classmethod
    def contains_input_type(cls, input_type: str) -> bool:
        return input_type in cls._value2member_map_


class InputField(BaseModel):
    type: InputFieldType
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class InputFieldPublic(InputField, FileRestrictions):
    pass


# App models


class AppCreateRequest(BaseModel):
    name: str


class AppPublic(AppCreateRequest, InDB, ResourcePermissionsMixin):
    description: str | None
    input_fields: list[InputFieldPublic]
    attachments: list[FilePublic]
    prompt: PromptPublic | None
    completion_model: CompletionModelSparse
    completion_model_kwargs: ModelKwargs
    allowed_attachments: FileRestrictions
    published: bool


@partial_model
class AppUpdateRequest(BaseModel):
    name: str
    description: str
    input_fields: list[InputField]
    attachments: list[ModelId]
    prompt: PromptCreate
    completion_model: ModelId
    completion_model_kwargs: ModelKwargs
