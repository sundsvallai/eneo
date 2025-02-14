from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID
    from intric.integration.domain.repositories.tenant_integration_repo import (
        TenantIntegrationRepository,
    )
    from intric.integration.domain.entities.tenant_integration import TenantIntegration


class TenantIntegrationService:
    def __init__(self, tenant_integration_repo: "TenantIntegrationRepository"):
        self.tenant_integration_repo = tenant_integration_repo

    async def get_tenant_integrations(self, tenant_id: "UUID") -> list["TenantIntegration"]:
        return await self.tenant_integration_repo.get_integrations_by_tenant_id(tenant_id=tenant_id)
