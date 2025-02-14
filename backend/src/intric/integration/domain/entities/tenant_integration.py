from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID

    from intric.integration.domain.entities.integration import Integration


class TenantIntegration:
    def __init__(
        self,
        id: "UUID",
        tenant_id: "UUID",
        integration: "Integration",
        enabled: bool = False,
    ):
        self.id = id
        self.tenant_id = tenant_id
        self.integration = integration
        self.enabled = enabled

    def toggle(self, enabled: bool) -> None:
        self.enabled = enabled
