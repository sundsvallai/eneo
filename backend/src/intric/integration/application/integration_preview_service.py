from typing import TYPE_CHECKING, List
from uuid import UUID

from intric.integration.domain.entities.integration_preview import IntegrationPreview
from intric.main.logging import get_logger

if TYPE_CHECKING:
    from intric.integration.domain.repositories.oauth_token_repo import (
        OauthTokenRepository,
    )
    from intric.integration.domain.repositories.user_integration_repo import (
        UserIntegrationRepository,
    )
    from intric.integration.infrastructure.preview_service.confluence_preview_service import (
        ConfluencePreviewService,
    )
    from intric.integration.infrastructure.preview_service.sharepoint_preview_service import (
        SharePointPreviewService,
    )


logger = get_logger(__name__)


class IntegrationPreviewService:
    def __init__(
        self,
        oauth_token_repo: "OauthTokenRepository",
        user_integration_repo: "UserIntegrationRepository",
        confluence_preview_service: "ConfluencePreviewService",
        sharepoint_preview_service: "SharePointPreviewService",
    ):
        self.oauth_token_repo = oauth_token_repo
        self.user_integration_repo = user_integration_repo
        self.confluence_preview_service = confluence_preview_service
        self.sharepoint_preview_service = sharepoint_preview_service

    async def get_preview_data(
        self,
        user_integration_id: UUID,
    ) -> List[IntegrationPreview]:
        user_integration = await self.user_integration_repo.one(id=user_integration_id)
        if not user_integration.authenticated:
            return []

        token = await self.oauth_token_repo.one(user_integration_id=user_integration_id)

        if token.token_type.is_confluence:
            return await self.confluence_preview_service.get_preview_info(
                token=token
            )
        elif token.token_type.is_sharepoint:
            return await self.sharepoint_preview_service.get_preview_info(
                token=token
            )
        else:
            raise ValueError(f"Unsupported integration type: {token.token_type}")
