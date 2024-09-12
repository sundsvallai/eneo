# MIT License

from datetime import datetime
from uuid import UUID

from pydantic import AliasPath, BaseModel, Field


class AssistantMetadata(BaseModel):
    id: UUID
    created_at: datetime


class SessionMetadata(AssistantMetadata):
    assistant_id: UUID = Field(validation_alias=AliasPath("assistant", "id"))


class QuestionMetadata(SessionMetadata):
    assistant_id: UUID
    session_id: UUID


class MetadataStatistics(BaseModel):
    assistants: list[AssistantMetadata]
    sessions: list[SessionMetadata]
    questions: list[QuestionMetadata]


class Counts(BaseModel):
    assistants: int
    sessions: int
    questions: int


class AskAnalysis(BaseModel):
    question: str
    completion_model_id: UUID | None = None
    stream: bool = False


class AnalysisAnswer(BaseModel):
    answer: str
