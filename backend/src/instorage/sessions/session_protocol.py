from instorage.questions.question_protocol import to_question_public
from instorage.sessions.session import (
    SessionFeedback,
    SessionInDB,
    SessionMetadataPublic,
    SessionPublic,
)


def to_session_public(session: SessionInDB):
    if session.feedback_value is not None:
        feedback = SessionFeedback(
            value=session.feedback_value, text=session.feedback_text
        )
    else:
        feedback = None

    return SessionPublic(
        **session.model_dump(),
        messages=[to_question_public(question) for question in session.questions],
        feedback=feedback
    )


def to_session_metadata_public(session: SessionInDB):
    return SessionMetadataPublic(**session.model_dump())
