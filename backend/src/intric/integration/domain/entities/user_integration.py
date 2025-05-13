from typing import TYPE_CHECKING, Optional
from uuid import UUID

from intric.base.base_entity import Entity

if TYPE_CHECKING:
    from intric.integration.domain.entities.tenant_integration import TenantIntegration


class UserIntegration(Entity):
    def __init__(
        self,
        user_id: UUID,
        tenant_integration: "TenantIntegration",
        id: Optional[UUID] = None,
        authenticated: bool = False,
    ):
        super().__init__(id=id)
        self.user_id = user_id
        self.tenant_integration = tenant_integration
        self.authenticated = authenticated

    @property
    def integration_type(self) -> str:
        return self.tenant_integration.integration.integration_type
