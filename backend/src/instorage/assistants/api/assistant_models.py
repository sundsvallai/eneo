from typing import AsyncIterable, Optional
from uuid import UUID

from pydantic import AliasChoices, AliasPath, ConfigDict, Field, field_validator

from instorage.ai_models.completion_models.completion_model import (
    CompletionModel,
    CompletionModelSparse,
    ModelKwargs,
)
from instorage.ai_models.embedding_models.embedding_model import EmbeddingModel
from instorage.files.file_models import File
from instorage.groups.group import GroupInDBBase, GroupSparse
from instorage.info_blobs.info_blob import InfoBlobInDBNoText
from instorage.main.config import get_settings
from instorage.main.models import (
    BaseModel,
    InDB,
    ModelId,
    ResourcePermissionsMixin,
    partial_model,
)
from instorage.sessions.session import SessionInDB
from instorage.users.user import UserSparse
from instorage.websites.website_models import WebsiteSparse


# Relationship models
class GroupWithEmbeddingModel(GroupInDBBase):
    embedding_model: Optional[EmbeddingModel] = None


# Models
class AssistantGuard(BaseModel):
    guardrail_active: bool = True
    guardrail_string: str = ""
    on_fail_message: str = "Jag kan tyvärr inte svara på det. Fråga gärna något annat!"


class AssistantBase(BaseModel):
    name: str
    prompt: str
    completion_model_kwargs: ModelKwargs = ModelKwargs()
    logging_enabled: bool = False

    @field_validator("completion_model_kwargs", mode="before")
    @classmethod
    def set_model_kwargs(cls, model_kwargs):
        return model_kwargs or ModelKwargs()


class AssistantCreatePublic(AssistantBase):
    groups: list[ModelId] = []
    websites: list[ModelId] = []
    guardrail: Optional[AssistantGuard] = None
    completion_model: ModelId


@partial_model
class AssistantUpdatePublic(AssistantCreatePublic):
    pass


class AssistantCreate(AssistantBase):
    user_id: UUID
    groups: list[ModelId] = []
    websites: list[ModelId] = []
    guardrail_active: Optional[bool] = None
    completion_model_id: UUID = Field(
        validation_alias=AliasChoices(
            AliasPath("completion_model", "id"), "completion_model_id"
        )
    )


@partial_model
class AssistantUpdate(AssistantCreate):
    id: UUID


class AssistantInDBBase(InDB, AssistantBase):
    space_id: Optional[UUID] = None
    completion_model_id: Optional[UUID] = None
    tenant_id: UUID = Field(validation_alias=AliasPath(["user", "tenant_id"]))


class AssistantPublicBase(InDB):
    name: str
    prompt: str
    completion_model_kwargs: Optional[ModelKwargs] = None
    logging_enabled: bool
    space_id: Optional[UUID] = None


class AskAssistant(BaseModel):
    question: str
    files: list[ModelId] = Field(max_length=get_settings().max_in_question, default=[])
    stream: bool = False


class AssistantResponse(BaseModel):
    session: SessionInDB
    question: str
    files: list[File]
    answer: str | AsyncIterable[str]
    info_blobs: list[InfoBlobInDBNoText]
    completion_model: Optional[CompletionModel] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class AssistantSparse(ResourcePermissionsMixin, AssistantBase, InDB):
    user_id: UUID
    is_published: bool = False


class CreateSpaceAssistant(AssistantCreate):
    space_id: UUID
    completion_model_id: Optional[UUID] = None


class AssistantPublic(InDB):
    name: str
    prompt: str
    space_id: Optional[UUID] = None
    completion_model_kwargs: ModelKwargs
    logging_enabled: bool
    groups: list[GroupSparse]
    websites: list[WebsiteSparse]
    completion_model: Optional[CompletionModelSparse]
    is_published: bool = False
    user: UserSparse
