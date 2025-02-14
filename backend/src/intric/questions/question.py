from typing import Optional
from uuid import UUID

from pydantic import AliasChoices, AliasPath, BaseModel, Field, model_validator

from intric.ai_models.completion_models.completion_model import CompletionModel
from intric.files.file_models import File, FilePublic
from intric.info_blobs.info_blob import InfoBlobInDB, InfoBlobPublicNoText
from intric.logging.logging import (
    LoggingDetails,
    LoggingDetailsInDB,
    LoggingDetailsPublic,
)
from intric.main.models import InDB, ModelId


# SubModels
class ToolAssistant(BaseModel):
    id: UUID
    at_tag: str = Field(
        validation_alias=AliasChoices("at-tag", "at_tag"), serialization_alias="at-tag"
    )


class Tools(BaseModel):
    assistants: list[ToolAssistant]


class UseTools(BaseModel):
    assistants: list[ModelId]


# Models
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
    tool_assistant_id: Optional[UUID] = None

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
    tools: UseTools


class MessageLogging(Message):
    logging_details: LoggingDetailsPublic
