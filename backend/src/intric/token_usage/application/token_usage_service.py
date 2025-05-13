from datetime import datetime, timedelta
from typing import Optional

from intric.roles.permissions import Permission, validate_permissions
from intric.token_usage.domain.token_usage_models import TokenUsageSummary
from intric.token_usage.infrastructure.token_usage_analyzer import TokenUsageAnalyzer
from intric.users.user import UserInDB


class TokenUsageService:
    """Service for analyzing and retrieving token usage data."""

    def __init__(self, user: UserInDB, token_usage_analyzer: TokenUsageAnalyzer):
        self.user = user
        self.token_usage_analyzer = token_usage_analyzer

    @validate_permissions(permission=Permission.ADMIN)
    async def get_token_usage(
        self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None
    ) -> TokenUsageSummary:
        """
        Get token usage statistics for the specified date range.
        If no dates are provided, returns data for the last 30 days.

        Args:
            start_date: The start date for the analysis period
            end_date: The end date for the analysis period

        Returns:
            A TokenUsageSummary object with aggregated token usage data
        """
        # Default to last 30 days if no dates provided
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()

        return await self.token_usage_analyzer.get_model_token_usage(
            tenant_id=self.user.tenant_id, start_date=start_date, end_date=end_date
        )
