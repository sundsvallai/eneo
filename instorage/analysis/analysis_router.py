# MIT License

from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sse_starlette import EventSourceResponse

from instorage.analysis import analysis_factory, analysis_protocol
from instorage.analysis.analysis import (
    AnalysisAnswer,
    AskAnalysis,
    Counts,
    MetadataStatistics,
)
from instorage.analysis.analysis_service import AnalysisService
from instorage.main.logging import get_logger
from instorage.main.models import PaginatedResponse
from instorage.questions import question_protocol
from instorage.questions.question import Message
from instorage.server import protocol

logger = get_logger(__name__)

router = APIRouter()


@router.get("/counts/", response_model=Counts)
async def get_counts(
    service: AnalysisService = Depends(analysis_factory.get_analysis_service),
):
    """Total counts."""
    return await service.get_tenant_counts()


@router.get("/metadata-statistics/")
async def get_metadata(
    start_date: datetime = datetime.now(timezone.utc) - timedelta(days=30),
    end_date: datetime = datetime.now(timezone.utc) + timedelta(hours=1, minutes=1),
    service: AnalysisService = Depends(analysis_factory.get_analysis_service),
) -> MetadataStatistics:
    """Data for analytics"""
    assistants, sessions, questions = await service.get_metadata_statistics(
        start_date, end_date
    )

    return analysis_protocol.to_metadata(
        assistants=assistants, sessions=sessions, questions=questions
    )


@router.get("/assistants/{assistant_id}/", response_model=PaginatedResponse[Message])
async def get_most_recent_questions(
    assistant_id: UUID,
    days_since: int = Query(ge=0, le=30, default=30),
    include_followups: bool = False,
    service: AnalysisService = Depends(analysis_factory.get_analysis_service),
):
    """Get all the questions asked to an assistant in the last `days_since` days.

    `days_since`: How long back in time to get the questions.

    `include_followups`: If not selected, only the first question of a session is returned.
        Order is by date ascending, but if followups are included they are grouped together
        with their original question.
    """
    questions = await service.get_questions_since(
        assistant_uuid=assistant_id,
        days=days_since,
        include_followups=include_followups,
    )

    return protocol.to_paginated_response(
        [question_protocol.to_question_public(question) for question in questions]
    )


@router.post("/assistants/{assistant_id}/")
async def ask_question_about_questions(
    assistant_id: UUID,
    ask_analysis: AskAnalysis,
    days_since: int = Query(ge=0, le=30, default=30),
    include_followups: bool = False,
    service: AnalysisService = Depends(
        analysis_factory.get_analysis_service_with_completion_model_service
    ),
):
    """Ask a question with the questions asked to an assistant in the last
      `days_since` days as the context.

    `days_since`: How long back in time to get the questions.

    `include_followups`: If not selected, only the first question of a session is returned.
        Order is by date ascending, but if followups are included they are grouped together
        with their original question.
    """
    ai_response = await service.ask_question_on_questions(
        question=ask_analysis.question,
        stream=ask_analysis.stream,
        assistant_uuid=assistant_id,
        days=days_since,
        include_followup=include_followups,
    )

    if ask_analysis.stream:

        async def event_stream():
            async for chunk in ai_response.completion:
                yield AnalysisAnswer(answer=chunk).model_dump_json()

        return EventSourceResponse(event_stream())

    return AnalysisAnswer(answer=ai_response.completion)
