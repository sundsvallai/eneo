from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID

    from intric.integration.domain.entities.user_integration import UserIntegration
    from intric.integration.domain.repositories.user_integration_repo import (
        UserIntegrationRepository,
    )


class UserIntegrationService:
    def __init__(self, user_integration_repo: "UserIntegrationRepository"):
        self.user_integration_repo = user_integration_repo

    async def get_user_integrations(self, user_id: "UUID") -> list["UserIntegration"]:
        return await self.user_integration_repo.get_integrations_by_user_id(
            user_id=user_id
        )
