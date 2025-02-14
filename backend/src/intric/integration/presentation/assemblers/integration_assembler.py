from typing import TYPE_CHECKING

from intric.integration.presentation.models import Integration as IntegrationModel
from intric.integration.presentation.models import IntegrationList

if TYPE_CHECKING:
    from intric.integration.domain.entities.integration import Integration


class IntegrationAssembler:

    @classmethod
    def from_domain_to_model(self, item: "Integration") -> "IntegrationModel":
        return IntegrationModel(id=item.id, name=item.name, description=item.description)

    @classmethod
    def to_paginated_response(
        self,
        integrations: list["Integration"],
    ) -> IntegrationList:
        items = [self.from_domain_to_model(integration) for integration in integrations]
        return IntegrationList(items=items)
