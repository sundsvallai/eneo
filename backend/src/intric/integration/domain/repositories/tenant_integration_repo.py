from typing import TYPE_CHECKING

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from intric.database.tables.integration_table import (
    TenantIntegration as TenantIntegrationDBModel,
)
from intric.integration.domain.factories.tenant_integration_factory import (
    TenantIntegrationFactory,
)

if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncSession

    from intric.integration.domain.entities.tenant_integration import TenantIntegration


class TenantIntegrationRepository:
    def __init__(self, session: "AsyncSession"):
        self.session = session
        self._db_model = TenantIntegrationDBModel

        self._options = [selectinload(self._db_model.integration)]

    async def get_integrations_by_tenant_id(
        self, tenant_id: "UUID"
    ) -> list["TenantIntegration"]:
        query = (
            select(self._db_model)
            .filter_by(tenant_id=tenant_id)
            .options(*self._options)
        )
        result = await self.session.scalars(query)
        result = result.all()

        if not result:
            return []

        return TenantIntegrationFactory.create_entities(records=result)
