from typing import TYPE_CHECKING

from intric.integration.domain.entities.user_integration import UserIntegration

if TYPE_CHECKING:
    from intric.database.tables.integration_table import (
        UserIntegration as UserIntegrationDBModel,
    )


class UserIntegrationFactory:
    @staticmethod
    def create_entity(record: "UserIntegrationDBModel") -> UserIntegration:
        return UserIntegration(
            id=record.id,
            authenticated=record.authenticated,
            tenant_integration=record.tenant_integration,
            user_id=record.user_id,
        )

    @staticmethod
    def create_entities(
        records: list["UserIntegrationDBModel"],
    ) -> list[UserIntegration]:
        return [
            UserIntegrationFactory.create_entity(record) for record in records
        ]
