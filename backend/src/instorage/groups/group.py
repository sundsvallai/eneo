from typing import Optional
from uuid import UUID

from pydantic import AliasChoices, AliasPath, BaseModel, Field

from instorage.ai_models.embedding_models.embedding_model import (
    EmbeddingModel,
    EmbeddingModelPublic,
)
from instorage.main.models import (
    IdAndName,
    InDB,
    ModelId,
    ResourcePermissionsMixin,
    partial_model,
)
from instorage.users.user import UserInDBBase, UserPublicBase


class GroupBase(BaseModel):
    name: str


class CreateGroupRequest(GroupBase):
    embedding_model: ModelId


@partial_model
class GroupUpdatePublic(GroupBase):
    pass


class GroupUpdate(GroupUpdatePublic):
    id: UUID


class GroupCreate(GroupBase):
    user_id: UUID
    tenant_id: UUID
    embedding_model_id: UUID = Field(
        validation_alias=AliasChoices(
            AliasPath("embedding_model", "id"), "embedding_model_id", "embedding_model"
        )
    )


class CreateSpaceGroup(GroupCreate):
    space_id: UUID
    embedding_model_id: UUID


class GroupInDBBase(InDB):
    space_id: Optional[UUID] = None
    name: str
    embedding_model_id: UUID
    user_id: UUID
    tenant_id: UUID


class GroupInDB(GroupInDBBase):
    user: UserInDBBase
    can_edit: Optional[bool] = None
    embedding_model: EmbeddingModel


class GroupMetadata(BaseModel):
    num_info_blobs: int


class GroupPublicBase(InDB, GroupBase):
    pass


class GroupPublic(GroupPublicBase):
    embedding_model: EmbeddingModelPublic


class GroupPublicWithMetadata(GroupPublic):
    metadata: GroupMetadata
    user: UserPublicBase
    can_edit: Optional[bool] = None


class DeletionInfo(BaseModel):
    success: bool


class DeleteGroupResponse(GroupPublic):
    deletion_info: DeletionInfo


class CreateGroupResponse(GroupPublic):
    pass


class GroupUpdateRequest(GroupBase):
    pass


class GroupSparse(ResourcePermissionsMixin, GroupBase, InDB):
    metadata: GroupMetadata
    user_id: UUID
    embedding_model: IdAndName
