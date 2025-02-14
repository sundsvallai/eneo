from typing import TYPE_CHECKING

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from intric.database.tables.integration_table import (
    TenantIntegration as TenantIntegrationDBModel,
)
from intric.database.tables.integration_table import (
    UserIntegration as UserIntegrationDBModel,
)
from intric.integration.domain.factories.user_integration_factory import (
    UserIntegrationFactory,
)

if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.ext.asyncio import AsyncSession

    from intric.integration.domain.entities.user_integration import UserIntegration


class UserIntegrationRepository:
    def __init__(self, session: "AsyncSession"):
        self.session = session
        self._db_model = UserIntegrationDBModel

        self._options = [
            selectinload(self._db_model.tenant_integration).selectinload(
                TenantIntegrationDBModel.integration
            )
        ]

    async def get_integrations_by_user_id(
        self, user_id: "UUID"
    ) -> list["UserIntegration"]:
        query = (
            select(self._db_model).filter_by(user_id=user_id).options(*self._options)
        )
        result = await self.session.scalars(query)
        result = result.all()

        if not result:
            return []

        return UserIntegrationFactory.create_entities(records=result)
