from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query

from intric.authentication.auth_dependencies import get_current_active_user
from intric.main.container.container import Container
from intric.server.dependencies.container import get_container
from intric.token_usage.presentation.token_usage_models import TokenUsageSummary

router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/", response_model=TokenUsageSummary)
async def get_token_usage(
    start_date: Optional[datetime] = Query(
        None,
        description="Start date for token usage data (defaults to 30 days ago)."
        "Time defaults to 00:00:00."
    ),
    end_date: Optional[datetime] = Query(
        None,
        description="End date for token usage data (defaults to current time)."
        "Time defaults to 00:00:00."
    ),
    container: Container = Depends(get_container(with_user=True)),
):
    """
    Get token usage statistics for the specified date range.
    If no dates are provided, returns token usage for the last 30 days.
    Note: If no time is provided in datetime parameters, time components default to 00:00:00.
    """
    token_usage_service = container.token_usage_service()

    usage_summary = await token_usage_service.get_token_usage(
        start_date=start_date, end_date=end_date
    )

    return TokenUsageSummary.from_domain(usage_summary)
