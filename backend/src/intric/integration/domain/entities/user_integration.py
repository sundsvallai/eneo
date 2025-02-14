from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uuid import UUID

    from intric.integration.domain.entities.tenant_integration import TenantIntegration


class UserIntegration:
    def __init__(
        self,
        id: "UUID",
        user_id: "UUID",
        tenant_integration: "TenantIntegration",
        authenticated: bool = False,
    ):
        self.id = id
        self.user_id = user_id
        self.tenant_integration = tenant_integration
        self.authenticated = authenticated

    def is_connected(self) -> bool:
        return self.authenticated
