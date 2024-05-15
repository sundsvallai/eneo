from typing import Optional
from uuid import UUID

from pydantic import AliasPath, BaseModel, ConfigDict, Field, model_validator

from instorage.ai_models.completion_models.llms import CompletionModel
from instorage.info_blobs.info_blob import InfoBlobInDB, InfoBlobPublicNoText
from instorage.logging.logging import (
    LoggingDetails,
    LoggingDetailsInDB,
    LoggingDetailsPublic,
)
from instorage.main.models import DateTimeModelMixin, IdWithUuidMixin


class QuestionBase(BaseModel):
    question: str
    answer: str


class QuestionAdd(QuestionBase):
    model: Optional[str] = None
    session_id: Optional[int] = None
    service_id: Optional[int] = None
    logging_details: Optional[LoggingDetails] = None

    @model_validator(mode="after")
    def require_one_of_session_id_and_service_id(self) -> "QuestionAdd":
        if self.service_id is None and self.session_id is None:
            raise ValueError("One of 'service_id' and 'session_id' is required")

        return self


class QuestionInDB(QuestionAdd, IdWithUuidMixin, DateTimeModelMixin):
    logging_details: Optional[LoggingDetailsInDB] = None
    info_blobs: list[InfoBlobInDB] = []
    assistant_uuid: Optional[UUID] = Field(
        validation_alias=AliasPath(["assistant", "uuid"]), default=None
    )
    session_uuid: Optional[UUID] = Field(
        validation_alias=AliasPath(["session", "uuid"]), default=None
    )

    model_config = ConfigDict(from_attributes=True)


class Message(QuestionBase, DateTimeModelMixin):
    id: UUID
    completion_model: Optional[CompletionModel] = None
    references: list[InfoBlobPublicNoText]


class MessageLogging(Message):
    logging_details: LoggingDetailsPublic
