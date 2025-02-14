from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from intric.main.models import InDB, Status


class Task(str, Enum):
    UPLOAD_FILE = "upload_info_blob"
    TRANSCRIPTION = "transcription"
    CRAWL = "crawl"
    EMBED_GROUP = "embed_group"
    CRAWL_ALL_WEBSITES = "crawl_all_websites"
    RUN_APP = "run_app"


class JobBase(BaseModel):
    name: Optional[str] = None
    status: Status
    task: Task
    result_location: Optional[str] = None
    finished_at: Optional[datetime] = None


class Job(JobBase):
    user_id: UUID


class JobUpdate(BaseModel):
    status: Optional[Status] = None
    result_location: Optional[str] = None
    finished_at: Optional[datetime] = None


class JobInDb(Job, InDB):
    pass


class JobPublic(JobBase, InDB):
    pass
