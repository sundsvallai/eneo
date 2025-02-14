from typing import TYPE_CHECKING

from intric.integration.presentation.models import UserIntegration as UserIntegrationModel
from intric.integration.presentation.models import UserIntegrationList

if TYPE_CHECKING:
    from intric.integration.domain.entities.user_integration import UserIntegration


class UserIntegrationAssembler:
    @classmethod
    def from_domain_to_model(cls, item: "UserIntegration") -> "UserIntegrationModel":
        return UserIntegrationModel(
            id=item.id,
            connected=item.authenticated,
            name=item.tenant_integration.integration.name,
            description=item.tenant_integration.integration.description,
        )

    @classmethod
    def to_paginated_response(
        cls,
        integrations: list["UserIntegration"],
    ) -> UserIntegrationList:
        items = [cls.from_domain_to_model(integration) for integration in integrations]
        return UserIntegrationList(items=items)
