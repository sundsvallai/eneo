from typing import TYPE_CHECKING

from intric.integration.presentation.models import TenantIntegration as TenantIntegrationModel
from intric.integration.presentation.models import TenantIntegrationList

if TYPE_CHECKING:
    from intric.integration.domain.entities.tenant_integration import TenantIntegration


class TenantIntegrationAssembler:
    @classmethod
    def from_domain_to_model(
        cls, item: "TenantIntegration"
    ) -> "TenantIntegrationModel":
        return TenantIntegrationModel(
            id=item.id,
            enabled=item.enabled,
            name=item.integration.name,
            description=item.integration.description,
        )

    @classmethod
    def to_paginated_response(
        cls,
        integrations: list["TenantIntegration"],
    ) -> TenantIntegrationList:
        items = [cls.from_domain_to_model(integration) for integration in integrations]
        return TenantIntegrationList(items=items)
