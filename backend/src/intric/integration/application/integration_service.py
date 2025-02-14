from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from intric.integration.domain.entities.integration import Integration
    from intric.integration.domain.repositories.integration_repo import IntegrationRepository


class IntegrationService:
    def __init__(self, integration_repo: "IntegrationRepository"):
        self.integration_repo = integration_repo

    async def get_integrations(self) -> list["Integration"]:
        return await self.integration_repo.all()
