# MIT License

from intric.analysis.analysis import (
    AssistantMetadata,
    MetadataStatistics,
    QuestionMetadata,
    SessionMetadata,
)
from intric.assistants.assistant import Assistant
from intric.questions.question import Question
from intric.sessions.session import SessionInDB


def to_metadata(
    assistants: list[Assistant],
    sessions: list[SessionInDB],
    questions: list[Question],
):
    assistants_metadata = [
        AssistantMetadata(
            id=assistant.id,
            created_at=assistant.created_at,
        )
        for assistant in assistants
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
