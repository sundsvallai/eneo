from typing import TYPE_CHECKING, Literal, Optional
from uuid import UUID

from pydantic import BaseModel

from intric.ai_models.completion_models.completion_model import CompletionModelPublic
from intric.files.file_models import FilePublic
from intric.info_blobs.info_blob import InfoBlobAskAssistantPublic
from intric.main.models import DateTimeModelMixin, InDB
from intric.questions.question import Message, Question, UseTools

if TYPE_CHECKING:
    from intric.assistants.api.assistant_models import AssistantSparse


class SessionFeedback(BaseModel):
    value: Literal[-1, 1]
    text: Optional[str] = None


class SessionBase(BaseModel):
    name: str


class SessionAdd(SessionBase):
    user_id: UUID
    assistant_id: UUID


class SessionUpdate(SessionBase):
    id: UUID


class SessionInDB(SessionBase, InDB):
    user_id: UUID
    feedback_value: Optional[Literal[-1, 1]] = None
    feedback_text: Optional[str] = None

    questions: list[Question] = []
    assistant: Optional["AssistantSparse"] = None


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
    question: str
    files: list[FilePublic]
    answer: str
    references: list[InfoBlobAskAssistantPublic]
    model: Optional[CompletionModelPublic] = None
    tools: UseTools


class SessionResponse(BaseModel):
    sessions: list[SessionId]
