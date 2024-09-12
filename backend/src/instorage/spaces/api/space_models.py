# MIT license

from enum import Enum
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel

from instorage.ai_models.completion_models.completion_model import (
    CompletionModelSparse,
    ModelKwargs,
)
from instorage.ai_models.embedding_models.embedding_model import EmbeddingModelSparse
from instorage.assistants.api.assistant_models import AssistantSparse
from instorage.groups.group import GroupMetadata, GroupSparse
from instorage.main.models import (
    InDB,
    ModelId,
    PaginatedPermissions,
    ResourcePermissionsMixin,
    partial_model,
)
from instorage.services.service import ServiceSparse
from instorage.users.user import UserSparse
from instorage.websites.crawl_dependencies.crawl_models import CrawlRunPublic, CrawlType
from instorage.websites.website_models import UpdateInterval, WebsiteSparse


class SpaceRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"


class CreateRequest(BaseModel):
    name: str


class TransferRequest(BaseModel):
    target_space_id: UUID


class TransferApplicationRequest(TransferRequest):
    move_resources: bool = False


# Members


class SpaceMember(UserSparse):
    role: SpaceRole


# Spaces


class CreateSpaceRequest(CreateRequest):
    pass


@partial_model
class UpdateSpaceRequest(BaseModel):
    name: str
    description: str

    embedding_models: list[ModelId]
    completion_models: list[ModelId]


class Applications(BaseModel):
    assistants: PaginatedPermissions[AssistantSparse]
    services: PaginatedPermissions[ServiceSparse]


class Knowledge(BaseModel):
    groups: PaginatedPermissions[GroupSparse]
    websites: PaginatedPermissions[WebsiteSparse]


class SpaceSparse(InDB):
    name: str
    description: Optional[str]
    personal: bool


class SpaceDashboard(ResourcePermissionsMixin, SpaceSparse):
    applications: Applications


class SpacePublic(SpaceDashboard):
    embedding_models: list[EmbeddingModelSparse]

    completion_models: list[CompletionModelSparse]
    knowledge: Knowledge
    members: PaginatedPermissions[SpaceMember]


# Assistants


class CreateSpaceAssistantRequest(CreateRequest):
    pass


class CreateSpaceServiceRequest(CreateRequest):
    pass


class CreateSpaceServiceResponse(InDB):
    name: str
    prompt: str
    completion_model_kwargs: ModelKwargs
    output_format: Optional[Literal["json", "list", "boolean"]] = None
    json_schema: Optional[dict] = None

    groups: list[GroupSparse]
    completion_model: Optional[CompletionModelSparse]
    is_published: bool = False
    can_edit: bool
    user: UserSparse


# Groups


class CreateSpaceGroupsRequest(CreateRequest):
    embedding_model: Optional[ModelId] = None


class CreateSpaceGroupsResponse(InDB):
    name: str
    embedding_model: Optional[EmbeddingModelSparse]
    user: UserSparse
    can_edit: bool
    metadata: GroupMetadata


# Websites


class CreateSpaceWebsitesRequest(BaseModel):
    name: Optional[str] = None
    url: str
    download_files: bool = False
    crawl_type: CrawlType = CrawlType.CRAWL
    update_interval: UpdateInterval = UpdateInterval.NEVER
    embedding_model: Optional[ModelId] = None


class CreateSpaceWebsitesResponse(InDB):
    name: str
    url: str

    download_files: bool
    crawl_type: CrawlType
    update_interval: UpdateInterval

    embedding_model: Optional[EmbeddingModelSparse]
    latest_crawl: Optional[CrawlRunPublic]


# Members


class AddSpaceMemberRequest(BaseModel):
    id: UUID
    role: SpaceRole


class UpdateSpaceMemberRequest(BaseModel):
    role: SpaceRole
