from enum import Enum
from typing import Generic, Literal, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, computed_field

from intric.ai_models.embedding_models.embedding_model import (
    EmbeddingModelPublicLegacy,
)
from intric.jobs.task_models import ResourceTaskParams
from intric.main.models import ResourcePermission

T = TypeVar("T", bound=BaseModel)


class BaseListModel(BaseModel, Generic[T]):
    items: list[T]

    @computed_field
    def count(self) -> int:
        return len(self.items)


class IntegrationType(str, Enum):
    Confluence = "confluence"
    Sharepoint = "sharepoint"

    @property
    def is_confluence(self) -> bool:
        return self == IntegrationType.Confluence

    @property
    def is_sharepoint(self) -> bool:
        return self == IntegrationType.Sharepoint


class Integration(BaseModel):
    id: UUID
    name: str
    description: str
    integration_type: IntegrationType


class IntegrationList(BaseListModel[Integration]):
    pass


class TenantIntegration(Integration):
    id: Optional[UUID] = None
    integration_id: UUID

    @computed_field
    def is_linked_to_tenant(self) -> bool:
        return self.id is not None


class TenantIntegrationList(BaseListModel[TenantIntegration]):
    pass


class TenantIntegrationFilter(Enum):
    DEFAULT = "all"
    TENANT_ONLY = "tenant_only"


class UserIntegration(Integration):
    id: Optional[UUID] = None
    tenant_integration_id: UUID
    connected: bool


class UserIntegrationList(BaseListModel[UserIntegration]):
    pass


class IntegrationCreate(BaseModel):
    name: str
    description: str
    integration_type: Literal["confluence", "sharepoint"]


class AuthUrlPublic(BaseModel):
    auth_url: str


class AuthCallbackParams(BaseModel):
    auth_code: str
    tenant_integration_id: UUID


class ConfluenceContentTaskParam(ResourceTaskParams):
    token_id: UUID
    space_key: str
    integration_knowledge_id: UUID


class SharepointContentTaskParam(ResourceTaskParams):
    token_id: UUID
    integration_knowledge_id: UUID
    site_id: str


class ConfluenceContentProcessParam(ResourceTaskParams):
    results: list


class IntegrationPreviewData(BaseModel):
    key: str
    type: str
    name: str
    url: str


class IntegrationPreviewDataList(BaseListModel[IntegrationPreviewData]):
    pass


class IntegrationKnowledgeMetaData(BaseModel):
    size: int


class IntegrationKnowledgePublic(BaseModel):
    id: UUID
    name: str
    url: str
    tenant_id: UUID
    space_id: UUID
    user_integration_id: UUID
    embedding_model: EmbeddingModelPublicLegacy
    permissions: list[ResourcePermission] = []
    metadata: IntegrationKnowledgeMetaData
    integration_type: Literal["confluence", "sharepoint"]
    task: Enum
