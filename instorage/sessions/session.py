from typing import TYPE_CHECKING, Literal, Optional
from uuid import UUID

from pydantic import BaseModel

from instorage.ai_models.completion_models.llms import CompletionModel
from instorage.info_blobs.info_blob import InfoBlobPublicNoText
from instorage.main.models import DateTimeModelMixin, InDB
from instorage.questions.question import Message, QuestionInDB

if TYPE_CHECKING:
    from instorage.assistants.assistant import AssistantInDBBase


class SessionFeedback(BaseModel):
    value: Literal[-1, 1]
    text: Optional[str] = None


class SessionBase(BaseModel):
    name: str


class SessionAdd(SessionBase):
    user_id: int
    assistant_id: int


class SessionUpdate(SessionBase):
    id: int


class SessionInDB(SessionAdd, InDB):
    assistant_id: Optional[int] = None
    feedback_value: Optional[Literal[-1, 1]] = None
    feedback_text: Optional[str] = None

    questions: list[QuestionInDB] = []
    assistant: "AssistantInDBBase" = None


class SessionUpdateRequest(SessionBase):
    id: UUID


class SessionMetadataPublic(SessionUpdateRequest, DateTimeModelMixin):
    pass


class SessionPublic(SessionMetadataPublic):
    messages: list[Message] = []
    feedback: Optional[SessionFeedback] = None


class SessionId(SessionUpdateRequest, DateTimeModelMixin):
    pass


class AskResponse(BaseModel):
    session_id: UUID
    answer: str
    references: list[InfoBlobPublicNoText]
    model: Optional[CompletionModel] = None


class SessionResponse(BaseModel):
    sessions: list[SessionId]
