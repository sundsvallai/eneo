from typing import TYPE_CHECKING

from sqlalchemy.future import select

from intric.database.tables.integration_table import Integration as IntegrationDBModel
from intric.integration.domain.factories.integration_factory import IntegrationFactory

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from intric.integration.domain.entities.integration import Integration


class IntegrationRepository:
    def __init__(self, session: "AsyncSession"):
        self.session = session
        self._db_model = IntegrationDBModel

    async def all(self) -> list["Integration"]:
        query = select(self._db_model)
        result = await self.session.scalars(query)
        result = result.all()
        if not result:
            return []

        integration = IntegrationFactory.create_entities(records=result)
        return integration
