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
            name=item.integration.name,
            description=item.integration.description,
            integration_type=item.integration.integration_type,
            integration_id=item.integration.id,
        )

    @classmethod
    def to_paginated_response(
        cls,
        integrations: list["TenantIntegration"],
    ) -> TenantIntegrationList:
        items = [cls.from_domain_to_model(integration) for integration in integrations]
        return TenantIntegrationList(items=items)
