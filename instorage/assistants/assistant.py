from typing import TYPE_CHECKING, AsyncIterator, Optional
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field, computed_field

from instorage.ai_models.completion_models.llms import (
    CompletionModel,
    CompletionModelName,
)
from instorage.groups.group import GroupId, GroupInDBBase, GroupPublicBase
from instorage.info_blobs.info_blob import InfoBlobInDBNoText
from instorage.main.models import InDB, Public
from instorage.sessions.session import SessionInDB
from instorage.users.user import (
    UserGroupInDBRead,
    UserGroupRead,
    UserInDBBase,
    UserPublicBase,
)

if TYPE_CHECKING:
    from instorage.workflows.workflow import StepInDB


class AssistantGuard(BaseModel):
    guardrail_active: bool = True
    guardrail_string: str = ""
    on_fail_message: str = "Jag kan tyvärr inte svara på det. Fråga gärna något annat!"


class AssistantBase(BaseModel):
    name: str
    prompt: str
    completion_model: CompletionModelName
    completion_model_kwargs: dict = {}
    logging_enabled: bool = False
    is_public: bool = False


class AssistantCreatePublic(AssistantBase):
    groups: Optional[list[GroupId]] = []
    guardrail: Optional[AssistantGuard] = None


class AssistantUpdatePublic(AssistantBase):
    name: Optional[str] = None
    prompt: Optional[str] = None
    completion_model: Optional[CompletionModelName] = None
    groups: Optional[list[GroupId]] = []
    guardrail: Optional[AssistantGuard] = None


class AssistantUpsert(AssistantUpdatePublic):
    id: Optional[int] = None
    uuid: Optional[UUID] = None
    user_id: Optional[int] = None
    guardrail_active: Optional[bool] = None
    completion_model: Optional[CompletionModelName] = None


class AssistantInDBBase(InDB, AssistantBase):
    tenant_id: int = Field(validation_alias=AliasPath(["user", "tenant_id"]))


class AssistantInDB(InDB, AssistantBase):
    user_id: int
    guardrail_active: Optional[bool] = None
    guard_step: Optional["StepInDB"] = None
    groups: list[GroupInDBBase]
    user_groups: list[UserGroupInDBRead] = []

    @computed_field
    @property
    def user_groups_ids(self) -> set[int]:
        return {user_group.id for user_group in self.user_groups}


class AssistantInDBWithUser(AssistantInDB):
    user: UserInDBBase
    can_edit: Optional[bool] = None


class AssistantPublicBase(Public):
    name: str
    prompt: str
    completion_model: CompletionModelName
    completion_model_kwargs: dict = {}
    logging_enabled: bool
    is_public: bool


class AssistantPublic(AssistantPublicBase):
    groups: list[GroupPublicBase]
    user_groups: list[UserGroupRead] = []
    guardrail: Optional[AssistantGuard] = None


class AssistantPublicWithUser(AssistantPublic):
    user: UserPublicBase
    can_edit: Optional[bool] = None


class AskAssistant(BaseModel):
    question: str
    stream: bool = False


class AssistantResponse(BaseModel):
    session: SessionInDB
    answer: str | AsyncIterator[str]
    info_blobs: list[InfoBlobInDBNoText]
    model: Optional[CompletionModel] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
