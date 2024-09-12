from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_serializer
from pydantic.networks import HttpUrl

from instorage.ai_models.embedding_models.embedding_model import (
    EmbeddingModel,
    EmbeddingModelPublicBase,
)
from instorage.main.models import (
    IdAndName,
    InDB,
    ModelId,
    ResourcePermissionsMixin,
    partial_model,
)
from instorage.websites.crawl_dependencies.crawl_models import (
    CrawlRunPublic,
    CrawlRunSparse,
    CrawlType,
)


class UpdateInterval(str, Enum):
    NEVER = "never"
    WEEKLY = "weekly"


class WebsiteBase(BaseModel):
    name: str
    url: str
    space_id: Optional[UUID] = None
    download_files: bool = False
    crawl_type: CrawlType = CrawlType.CRAWL
    update_interval: UpdateInterval = UpdateInterval.NEVER


class WebsiteCreateRequest(WebsiteBase):
    url: HttpUrl
    embedding_model: ModelId

    @field_serializer("url")
    def serialize_to_string(url: HttpUrl):
        return str(url)


class WebsiteCreate(WebsiteBase):
    user_id: UUID
    tenant_id: UUID
    embedding_model_id: UUID


@partial_model
class WebsiteUpdateRequest(WebsiteCreateRequest):
    pass


class WebsiteUpdate(WebsiteUpdateRequest, ModelId):
    url: Optional[str] = None


class WebsiteInDBBase(WebsiteCreate, InDB):
    space_id: Optional[UUID] = None
    embedding_model_id: Optional[UUID] = None


class Website(WebsiteInDBBase):
    latest_crawl: Optional[CrawlRunPublic] = None
    embedding_model: Optional[EmbeddingModel] = None


class WebsitePublic(WebsiteBase, InDB):
    latest_crawl: Optional[CrawlRunPublic] = None
    embedding_model: Optional[EmbeddingModelPublicBase] = None


class WebsiteSparse(ResourcePermissionsMixin, WebsiteBase, InDB):
    url: str
    latest_crawl: Optional[CrawlRunSparse] = None
    user_id: UUID
    embedding_model: IdAndName
