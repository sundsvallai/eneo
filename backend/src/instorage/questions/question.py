from typing import Optional
from uuid import UUID

from pydantic import AliasPath, BaseModel, Field, model_validator

from instorage.ai_models.completion_models.completion_model import CompletionModel
from instorage.files.file_models import File, FilePublic
from instorage.info_blobs.info_blob import InfoBlobInDB, InfoBlobPublicNoText
from instorage.logging.logging import (
    LoggingDetails,
    LoggingDetailsInDB,
    LoggingDetailsPublic,
)
from instorage.main.models import InDB


class QuestionBase(BaseModel):
    question: str
    answer: str


class QuestionAdd(QuestionBase):
    num_tokens_question: int
    num_tokens_answer: int
    tenant_id: UUID
    completion_model_id: Optional[UUID] = None
    session_id: Optional[UUID] = None
    service_id: Optional[UUID] = None
    logging_details: Optional[LoggingDetails] = None

    @model_validator(mode="after")
    def require_one_of_session_id_and_service_id(self) -> "QuestionAdd":
        if self.service_id is None and self.session_id is None:
            raise ValueError("One of 'service_id' and 'session_id' is required")

        return self


class Question(QuestionAdd, InDB):
    logging_details: Optional[LoggingDetailsInDB] = None
    info_blobs: list[InfoBlobInDB] = []
    assistant_id: Optional[UUID] = Field(
        validation_alias=AliasPath(["assistant", "id"]), default=None
    )
    session_id: Optional[UUID] = None
    completion_model: Optional[CompletionModel] = None
    files: list[File] = []


class Message(QuestionBase, InDB):
    completion_model: Optional[CompletionModel] = None
    references: list[InfoBlobPublicNoText]
    files: list[FilePublic]


class MessageLogging(Message):
    logging_details: LoggingDetailsPublic
