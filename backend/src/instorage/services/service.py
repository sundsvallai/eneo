from typing import Literal, Optional
from uuid import UUID

from pydantic import AliasChoices, AliasPath, BaseModel, Field, model_validator

from instorage.ai_models.completion_models.completion_model import (
    CompletionModel,
    CompletionModelPublic,
    ModelKwargs,
)
from instorage.groups.group import GroupInDBBase, GroupPublicBase
from instorage.info_blobs.info_blob import (
    InfoBlobChunkInDBWithScore,
    InfoBlobInDB,
    InfoBlobPublic,
)
from instorage.main.models import InDB, ModelId, ResourcePermissionsMixin, partial_model
from instorage.users.user import UserInDBBase, UserPublicBase


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
    completion_model_kwargs: Optional[ModelKwargs] = ModelKwargs()


class ServiceCreatePublic(ServiceBase):
    groups: list[ModelId] = []
    completion_model: ModelId


@partial_model
class ServiceUpdatePublic(ServiceCreatePublic):
    pass


class ServiceCreate(ServiceBase):
    user_id: UUID
    groups: list[ModelId] = []
    completion_model_id: UUID = Field(
        validation_alias=AliasChoices(
            AliasPath("completion_model", "id"), "completion_model_id"
        )
    )


@partial_model
class ServiceUpdate(ServiceCreate):
    id: UUID


class ServiceInDBBase(InDB, ServiceBase):
    tenant_id: UUID = Field(validation_alias=AliasPath(["user", "tenant_id"]))


class Service(InDB, ServiceBase):
    user_id: UUID
    space_id: Optional[UUID] = None
    groups: list[GroupInDBBase]
    completion_model_id: UUID
    completion_model: Optional[CompletionModel] = None
    user: UserInDBBase
    can_edit: bool = False


class ServicePublicBase(InDB, OutputValidation):
    name: str
    prompt: str
    completion_model_kwargs: Optional[ModelKwargs] = None
    space_id: Optional[UUID] = None


class ServicePublic(ServicePublicBase):
    groups: list[GroupPublicBase]
    completion_model: CompletionModelPublic


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
    completion_model: CompletionModelPublic
    references: list[InfoBlobPublic]


class DatastoreResult(BaseModel):
    chunks: list[InfoBlobChunkInDBWithScore]
    no_duplicate_chunks: list[InfoBlobChunkInDBWithScore]
    info_blobs: list[InfoBlobInDB]


class RunnerResult(BaseModel):
    result: bool | list | dict | str
    datastore_result: DatastoreResult


class ServiceSparse(ResourcePermissionsMixin, ServiceBase, InDB):
    user_id: UUID
    is_published: bool = False


class CreateSpaceService(ServiceCreate):
    space_id: UUID
    completion_model_id: Optional[UUID] = None
