# MIT License

from datetime import date, datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sse_starlette import EventSourceResponse

from intric.analysis import analysis_protocol
from intric.analysis.analysis import (
    AnalysisAnswer,
    AskAnalysis,
    Counts,
    MetadataStatistics,
)
from intric.main.container.container import Container
from intric.main.logging import get_logger
from intric.main.models import PaginatedResponse
from intric.questions import question_protocol
from intric.questions.question import Message
from intric.server import protocol
from intric.server.dependencies.container import get_container

logger = get_logger(__name__)

router = APIRouter()


@router.get("/counts/", response_model=Counts)
async def get_counts(container: Container = Depends(get_container(with_user=True))):
    """Total counts."""
    service = container.analysis_service()
    return await service.get_tenant_counts()


@router.get("/metadata-statistics/")
async def get_metadata(
    start_date: datetime = datetime.now(timezone.utc) - timedelta(days=30),
    end_date: datetime = datetime.now(timezone.utc) + timedelta(hours=1, minutes=1),
    container: Container = Depends(get_container(with_user=True)),
) -> MetadataStatistics:
    """Data for analytics"""
    service = container.analysis_service()
    assistants, sessions, questions = await service.get_metadata_statistics(
        start_date, end_date
    )

    return analysis_protocol.to_metadata(
        assistants=assistants, sessions=sessions, questions=questions
    )


@router.get("/assistants/{assistant_id}/", response_model=PaginatedResponse[Message])
async def get_most_recent_questions(
    assistant_id: UUID,
    days_since: int = Query(ge=0, le=90, default=30),
    from_date: date | None = None,
    to_date: date | None = None,
    include_followups: bool = False,
    container: Container = Depends(get_container(with_user=True)),
):
    """Get all the questions asked to an assistant in the last `days_since` days.

    `days_since`: How long back in time to get the questions.

    `include_followups`: If not selected, only the first question of a session is returned.
        Order is by date ascending, but if followups are included they are grouped together
        with their original question.
    """
    if from_date is None or to_date is None:
        to_date = date.today()
        from_date = to_date - timedelta(days=days_since)

    service = container.analysis_service()
    questions = await service.get_questions_since(
        assistant_id=assistant_id,
        from_date=from_date,
        to_date=to_date,
        include_followups=include_followups,
    )

    return protocol.to_paginated_response(
        [question_protocol.to_question_public(question) for question in questions]
    )


@router.post("/assistants/{assistant_id}/")
async def ask_question_about_questions(
    assistant_id: UUID,
    ask_analysis: AskAnalysis,
    days_since: int = Query(ge=0, le=90, default=30),
    from_date: date | None = None,
    to_date: date | None = None,
    include_followups: bool = False,
    container: Container = Depends(get_container(with_user=True)),
):
    """Ask a question with the questions asked to an assistant in the last
      `days_since` days as the context.

    `days_since`: How long back in time to get the questions.

    `include_followups`: If not selected, only the first question of a session is returned.
        Order is by date ascending, but if followups are included they are grouped together
        with their original question.
    """
    if from_date is None or to_date is None:
        to_date = date.today()
        from_date = to_date - timedelta(days=days_since)

    service = container.analysis_service()
    ai_response = await service.ask_question_on_questions(
        question=ask_analysis.question,
        stream=ask_analysis.stream,
        assistant_id=assistant_id,
        from_date=from_date,
        to_date=to_date,
        include_followup=include_followups,
    )

    if ask_analysis.stream:

        async def event_stream():
            async for chunk in ai_response.completion:
                yield AnalysisAnswer(answer=chunk).model_dump_json()

        return EventSourceResponse(event_stream())

    return AnalysisAnswer(answer=ai_response.completion)
