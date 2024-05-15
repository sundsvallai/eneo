from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, computed_field

from instorage.ai_models.embedding_models.embedding_models import EmbeddingModelName
from instorage.main.models import InDB, Public
from instorage.users.user import (
    UserGroupInDBRead,
    UserGroupRead,
    UserInDBBase,
    UserPublicBase,
)


class IndexType(str, Enum):
    HNSW = "hnsw"
    FLAT = "flat"


class GroupId(BaseModel):
    id: UUID


class GroupBase(BaseModel):
    name: str
    is_public: bool = False
    embedding_model: Optional[EmbeddingModelName] = None
    index_type: IndexType = IndexType.FLAT


class GroupUpdatePublic(BaseModel):
    name: Optional[str] = None
    is_public: Optional[bool] = None


class GroupUpdate(GroupUpdatePublic):
    id: int


class GroupCreate(GroupBase):
    user_id: int
    tenant_id: int
    embedding_model: EmbeddingModelName


class GroupInDBBase(InDB):
    name: str
    is_public: bool
    embedding_model: EmbeddingModelName
    index_type: IndexType
    user_id: int
    tenant_id: int


class GroupInDB(GroupInDBBase):
    user: UserInDBBase
    can_edit: Optional[bool] = None
    user_groups: list[UserGroupInDBRead] = []

    @computed_field
    @property
    def user_groups_ids(self) -> set[int]:
        return {user_group.id for user_group in self.user_groups}


class GroupPublicBase(Public):
    name: str
    is_public: bool
    embedding_model: EmbeddingModelName
    index_type: IndexType


class GroupPublic(GroupPublicBase):
    user_groups: list[UserGroupRead] = []


class GroupMetadata(BaseModel):
    num_info_blobs: int


class GroupPublicWithMetadata(GroupPublic):
    metadata: GroupMetadata
    user: UserPublicBase
    can_edit: Optional[bool] = None


class DeletionInfo(BaseModel):
    success: bool


class DeleteGroupResponse(GroupPublic):
    deletion_info: DeletionInfo


class CreateGroupRequest(GroupBase):
    pass


class CreateGroupResponse(GroupPublic):
    pass


class GroupUpdateRequest(GroupBase):
    pass
