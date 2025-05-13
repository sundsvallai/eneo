from typing import TYPE_CHECKING

from intric.integration.domain.entities.user_integration import (
    UserIntegration,
)
from intric.main.exceptions import UnauthorizedException

if TYPE_CHECKING:
    from uuid import UUID

    from intric.integration.domain.repositories.tenant_integration_repo import (
        TenantIntegrationRepository,
    )
    from intric.integration.domain.repositories.user_integration_repo import (
        UserIntegrationRepository,
    )
    from intric.users.user import UserInDB


class UserIntegrationService:
    def __init__(
        self,
        user_integration_repo: "UserIntegrationRepository",
        tenant_integration_repo: "TenantIntegrationRepository",
        user: "UserInDB",
    ):
        self.user_integration_repo = user_integration_repo
        self.tenant_integration_repo = tenant_integration_repo
        self.user = user

    async def get_my_integrations(
        self,
        user_id: "UUID",
        tenant_id: "UUID",
    ) -> list["UserIntegration"]:
        authenticated_list = await self.user_integration_repo.query(user_id=user_id)
        authenticated_id_map = {
            item.tenant_integration.id: item for item in authenticated_list
        }

        available = await self.tenant_integration_repo.query(tenant_id=tenant_id)

        results = []
        for a in available:
            user_integration = UserIntegration(user_id=user_id, tenant_integration=a)
            if a.id not in authenticated_id_map:
                results.append(user_integration)
            else:
                results.append(authenticated_id_map.get(a.id, user_integration))
        return results

    async def disconnect_integration(self, user_integration_id: "UUID") -> None:
        integration = await self.user_integration_repo.one(id=user_integration_id)
        if integration.user_id != self.user.id:
            raise UnauthorizedException()

        await self.user_integration_repo.remove(id=integration.id)
