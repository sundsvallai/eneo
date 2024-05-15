from enum import Enum
from typing import Optional

from pydantic import BaseModel

from instorage.main.models import InDB, Public


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


class Job(BaseModel):
    name: Optional[str] = None
    status: JobStatus
    task: Task
    result_location: Optional[str] = None
    user_id: int


class JobUpdate(BaseModel):
    status: Optional[JobStatus] = None
    result_location: Optional[str] = None


class JobInDb(Job, InDB):
    pass


class JobPublic(Job, Public):
    pass
