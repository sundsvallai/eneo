from uuid import UUID

from pydantic import BaseModel


class TaskParams(BaseModel):
    pass


class InfoBlobTask(TaskParams):
    user_id: UUID
    group_id: UUID


class UploadTask(InfoBlobTask):
    filepath: str
    filename: str


class UploadInfoBlob(UploadTask):
    pass


class Transcription(UploadTask):
    pass


class EmbedGroup(InfoBlobTask):
    pass
