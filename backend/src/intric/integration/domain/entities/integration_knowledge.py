from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from intric.base.base_entity import Entity

if TYPE_CHECKING:
    from intric.embedding_models.domain.embedding_model import EmbeddingModel
    from intric.integration.domain.entities.user_integration import UserIntegration


_DEFAULT_SIZE = 0


class IntegrationKnowledge(Entity):
    def __init__(
        self,
        name: str,
        user_integration: "UserIntegration",
        embedding_model: "EmbeddingModel",
        tenant_id: UUID,
        space_id: UUID,
        id: Optional[UUID] = None,
        size: int | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        url: str | None = None,
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.name = name
        self.url = url
        self.tenant_id = tenant_id
        self.space_id = space_id
        self.user_integration = user_integration
        self.embedding_model = embedding_model
        self.size = size or _DEFAULT_SIZE

    @property
    def integration_type(self) -> str:
        return self.user_integration.tenant_integration.integration.integration_type
