from typing import AsyncIterable, Optional
from uuid import UUID

from pydantic import (
    AliasChoices,
    AliasPath,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from intric.ai_models.completion_models.completion_model import (
    CompletionModel,
    CompletionModelSparse,
    ModelKwargs,
)
from intric.ai_models.embedding_models.embedding_model import EmbeddingModel
from intric.files.file_models import File, FilePublic, FileRestrictions
from intric.groups.api.group_models import GroupInDBBase, GroupPublicWithMetadata
from intric.info_blobs.info_blob import InfoBlobInDBNoText
from intric.main.config import get_settings
from intric.main.models import InDB, ModelId, ResourcePermissionsMixin, partial_model
from intric.prompts.api.prompt_models import PromptCreate, PromptPublic
from intric.questions.question import Tools, UseTools
from intric.sessions.session import SessionInDB
from intric.users.user import UserSparse
from intric.websites.website_models import WebsiteSparse


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
    completion_model_kwargs: ModelKwargs = ModelKwargs()
    logging_enabled: bool = False

    @field_validator("completion_model_kwargs", mode="before")
    @classmethod
    def set_model_kwargs(cls, model_kwargs):
        return model_kwargs or ModelKwargs()


class AssistantCreatePublic(AssistantBase):
    prompt: Optional[PromptCreate] = None
    space_id: UUID
    groups: list[ModelId] = []
    websites: list[ModelId] = []
    guardrail: Optional[AssistantGuard] = None
    completion_model: ModelId


@partial_model
class AssistantUpdatePublic(AssistantCreatePublic):
    prompt: Optional[PromptCreate] = None
    attachments: Optional[list[ModelId]] = None


class AssistantCreate(AssistantBase):
    prompt: Optional[PromptCreate] = None
    space_id: UUID
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


class AssistantPublicBase(InDB):
    name: str
    prompt: PromptCreate
    completion_model_kwargs: Optional[ModelKwargs] = None
    logging_enabled: bool
    space_id: Optional[UUID] = None


class AskAssistant(BaseModel):
    question: str
    files: list[ModelId] = Field(max_length=get_settings().max_in_question, default=[])
    stream: bool = False
    tools: Optional[UseTools] = None


class AssistantResponse(BaseModel):
    session: SessionInDB
    question: str
    files: list[File]
    answer: str | AsyncIterable[str]
    info_blobs: list[InfoBlobInDBNoText]
    completion_model: CompletionModel
    tools: UseTools

    model_config = ConfigDict(arbitrary_types_allowed=True)


class AssistantSparse(ResourcePermissionsMixin, AssistantBase, InDB):
    user_id: UUID
    published: bool = False


class AssistantPublic(InDB, ResourcePermissionsMixin):
    name: str
    prompt: Optional[PromptPublic] = None
    space_id: UUID
    completion_model_kwargs: ModelKwargs
    logging_enabled: bool
    attachments: list[FilePublic]
    allowed_attachments: FileRestrictions
    groups: list[GroupPublicWithMetadata]
    websites: list[WebsiteSparse]
    completion_model: CompletionModelSparse
    published: bool = False
    user: UserSparse
    tools: Tools


class DefaultAssistant(AssistantPublic):
    completion_model: Optional[CompletionModelSparse] = None


SessionInDB.model_rebuild()
