# MIT License

from datetime import datetime
from uuid import UUID

from pydantic import AliasPath, BaseModel, Field

from instorage.ai_models.completion_models.llms import CompletionModelName


class AssistantMetadata(BaseModel):
    id: UUID = Field(validation_alias="uuid")
    created_at: datetime


class SessionMetadata(AssistantMetadata):
    assistant_id: UUID = Field(validation_alias=AliasPath(["assistant", "uuid"]))


class QuestionMetadata(AssistantMetadata):
    assistant_id: UUID = Field(validation_alias="assistant_uuid")
    session_id: UUID = Field(validation_alias="session_uuid")


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
    completion_model: str = CompletionModelName.GPT_4
    stream: bool = False


class AnalysisAnswer(BaseModel):
    answer: str
