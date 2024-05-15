# MIT License

from instorage.analysis.analysis import (
    AssistantMetadata,
    MetadataStatistics,
    QuestionMetadata,
    SessionMetadata,
)
from instorage.assistants.assistant import AssistantInDB
from instorage.questions.question import QuestionInDB
from instorage.sessions.session import SessionInDB


def to_metadata(
    assistants: list[AssistantInDB],
    sessions: list[SessionInDB],
    questions: list[QuestionInDB],
):
    assistants_metadata = [
        AssistantMetadata(**assistant.model_dump()) for assistant in assistants
    ]
    sessions_metadata = [
        SessionMetadata(**session.model_dump()) for session in sessions
    ]
    questions_metadata = [
        QuestionMetadata(**question.model_dump()) for question in questions
    ]

    return MetadataStatistics(
        assistants=assistants_metadata,
        sessions=sessions_metadata,
        questions=questions_metadata,
    )
