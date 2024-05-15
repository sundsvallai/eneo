from typing import Literal, Optional
from uuid import UUID

from pydantic import AliasPath, BaseModel, Field, computed_field, model_validator

from instorage.ai_models.completion_models.llms import (
    CompletionModel,
    CompletionModelName,
)
from instorage.groups.group import GroupId, GroupInDBBase, GroupPublic
from instorage.info_blobs.info_blob import (
    InfoBlobChunkInDBWithScore,
    InfoBlobInDB,
    InfoBlobPublic,
)
from instorage.main.models import InDB, Public
from instorage.users.user import (
    UserGroupInDBRead,
    UserGroupRead,
    UserInDBBase,
    UserPublicBase,
)


class OutputValidation(BaseModel):
    output_format: Optional[Literal["json", "list", "boolean"]] = None
    json_schema: Optional[dict] = None

    @model_validator(mode="after")
    def require_json_schema_if_output_format_is_json(self):
        if self.output_format == "json" and self.json_schema is None:
            raise ValueError("json_schema is requred if output_format is 'json'")

        return self


class ServiceBase(OutputValidation):
    name: str
    prompt: str
    completion_model: CompletionModelName
    completion_model_kwargs: dict = {}
    logging_enabled: bool = False
    is_public: bool = False


class ServiceCreatePublic(ServiceBase):
    groups: list[GroupId] = []
    completion_model: CompletionModelName


class ServiceUpdatePublic(ServiceCreatePublic):
    name: Optional[str] = None
    prompt: Optional[str] = None
    completion_model: Optional[CompletionModelName] = None


class ServiceUpsert(ServiceUpdatePublic):
    id: Optional[int] = None
    uuid: Optional[UUID] = None
    user_id: Optional[int] = None
    completion_model: Optional[CompletionModelName] = None


class ServiceInDBBase(InDB, ServiceBase):
    tenant_id: int = Field(validation_alias=AliasPath(["user", "tenant_id"]))


class ServiceInDB(InDB, ServiceBase):
    user_id: int
    groups: list[GroupInDBBase]
    user_groups: list[UserGroupInDBRead] = []

    @computed_field
    @property
    def user_groups_ids(self) -> set[int]:
        return {user_group.id for user_group in self.user_groups}


class ServiceInDBWithUser(ServiceInDB):
    user: UserInDBBase
    can_edit: Optional[bool] = None


class ServicePublicBase(Public, OutputValidation):
    name: str
    prompt: str
    completion_model: CompletionModelName
    completion_model_kwargs: dict = {}
    logging_enabled: bool
    is_public: bool


class ServicePublic(ServicePublicBase):
    groups: list[GroupPublic]
    user_groups: list[UserGroupRead] = []


class ServicePublicWithUser(ServicePublic):
    user: UserPublicBase
    can_edit: Optional[bool] = None


class RunService(BaseModel):
    input: str


class ServiceOutput(BaseModel):
    output: dict | list | str


class ServiceRun(BaseModel):
    id: UUID
    input: str
    output: dict | list | str
    completion_model: CompletionModel
    references: list[InfoBlobPublic]


class DatastoreResult(BaseModel):
    chunks: list[InfoBlobChunkInDBWithScore]
    no_duplicate_chunks: list[InfoBlobChunkInDBWithScore]
    info_blobs: list[InfoBlobInDB]


class RunnerResult(BaseModel):
    result: bool | list | dict | str
    datastore_result: DatastoreResult
