from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from instorage.main.models import InDB


class JobStatus(str, Enum):
    IN_PROGRESS = "in progress"
    QUEUED = "queued"
    COMPLETE = "complete"
    FAILED = "failed"
    NOT_FOUND = "not found"


class Task(str, Enum):
    UPLOAD_FILE = "upload_info_blob"
    TRANSCRIPTION = "transcription"
    CRAWL = "crawl"
    EMBED_GROUP = "embed_group"
    CRAWL_ALL_WEBSITES = "crawl_all_websites"


class JobBase(BaseModel):
    name: Optional[str] = None
    status: JobStatus
    task: Task
    result_location: Optional[str] = None
    finished_at: Optional[datetime] = None


class Job(JobBase):
    user_id: UUID


class JobUpdate(BaseModel):
    status: Optional[JobStatus] = None
    result_location: Optional[str] = None
    finished_at: Optional[datetime] = None


class JobInDb(Job, InDB):
    pass


class JobPublic(JobBase, InDB):
    pass
