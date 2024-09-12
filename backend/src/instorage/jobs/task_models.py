from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TaskParams(BaseModel):
    user_id: UUID
    group_id: Optional[UUID] = None
    website_id: Optional[UUID] = None


class InfoBlobTask(TaskParams):
    group_id: UUID


class UploadTask(InfoBlobTask):
    filepath: str
    filename: str
    mimetype: str


class UploadInfoBlob(UploadTask):
    pass


class Transcription(UploadTask):
    pass


class EmbedGroup(InfoBlobTask):
    pass
