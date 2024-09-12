from typing import TYPE_CHECKING, Literal, Optional
from uuid import UUID

from pydantic import BaseModel

from instorage.ai_models.completion_models.completion_model import CompletionModelPublic
from instorage.files.file_models import FilePublic
from instorage.info_blobs.info_blob import InfoBlobPublicNoText
from instorage.main.models import DateTimeModelMixin, InDB
from instorage.questions.question import Message, Question

if TYPE_CHECKING:
    from instorage.assistants.api.assistant_models import AssistantInDBBase


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
    assistant: Optional["AssistantInDBBase"] = None


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
    references: list[InfoBlobPublicNoText]
    model: Optional[CompletionModelPublic] = None


class SessionResponse(BaseModel):
    sessions: list[SessionId]
