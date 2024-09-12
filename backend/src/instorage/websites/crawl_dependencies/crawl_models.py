from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import AliasChoices, AliasPath, BaseModel, Field, field_serializer
from pydantic.networks import HttpUrl

from instorage.groups.group import GroupInDBBase, GroupPublicBase
from instorage.jobs.job_models import JobStatus
from instorage.jobs.task_models import TaskParams
from instorage.main.models import InDB, ModelId, partial_model


class CrawlType(str, Enum):
    CRAWL = "crawl"
    SITEMAP = "sitemap"


class CrawlBase(BaseModel):
    name: str
    url: str
    download_files: bool = False
    crawl_type: CrawlType = CrawlType.CRAWL


class CrawlCreateRequest(CrawlBase):
    group: ModelId
    url: HttpUrl

    @field_serializer("url")
    def serialize_to_string(url: HttpUrl):
        return str(url)


class CrawlCreate(CrawlBase):
    group_id: UUID = Field(validation_alias=AliasPath("group", "id"))
    user_id: UUID
    tenant_id: UUID
    update_interval: str = "never"
    embedding_model_id: UUID


@partial_model
class CrawlUpdateRequest(CrawlCreateRequest):
    pass


class CrawlUpdate(CrawlUpdateRequest, ModelId):
    url: Optional[str] = None
    group_id: Optional[UUID] = Field(
        validation_alias=AliasPath("group", "id"), default=None
    )


class CrawlInDB(CrawlBase, InDB):
    tenant_id: UUID
    group: Optional[GroupInDBBase] = None


class CrawlPublic(CrawlBase, InDB):
    group: Optional[GroupPublicBase]


class CrawlParams(BaseModel):
    group_id: ModelId


class CrawlTask(TaskParams):
    website_id: Optional[UUID] = None
    group_id: Optional[UUID] = None
    run_id: UUID
    url: str
    download_files: bool = False
    crawl_type: CrawlType = CrawlType.CRAWL


class CrawlRunBase(BaseModel):
    pages_crawled: Optional[int] = None
    files_downloaded: Optional[int] = None
    pages_failed: Optional[int] = None
    files_failed: Optional[int] = None


class CrawlRunCreate(BaseModel):
    website_id: UUID
    tenant_id: UUID


class CrawlRunUpdate(CrawlRunBase):
    id: UUID
    job_id: Optional[UUID] = None


class CrawlRunSparse(CrawlRunBase, InDB):
    status: Optional[JobStatus] = Field(
        validation_alias=AliasChoices(AliasPath("job", "status"), "status"),
        default=JobStatus.QUEUED,
    )
    result_location: Optional[str] = Field(
        validation_alias=AliasChoices(
            AliasPath("job", "result_location"), "result_location"
        ),
        default=None,
    )
    finished_at: Optional[datetime] = Field(
        validation_alias=AliasChoices(AliasPath("job", "finished_at"), "finished_at"),
        default=None,
    )


class CrawlRun(CrawlRunSparse):
    website_id: UUID
    tenant_id: UUID


class CrawlRunPublic(CrawlRunSparse):
    pass
