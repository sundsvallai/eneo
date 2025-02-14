from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from intric.database.tables.ai_models_table import CompletionModels, EmbeddingModels
from intric.database.tables.base_class import BaseCrossReference, BasePublic
from intric.database.tables.tenant_table import Tenants
from intric.database.tables.users_table import Users

if TYPE_CHECKING:
    from intric.database.tables.app_table import Apps
    from intric.database.tables.assistant_table import Assistants
    from intric.database.tables.groups_table import Groups
    from intric.database.tables.service_table import Services
    from intric.database.tables.websites_table import Websites


class Spaces(BasePublic):
    name: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column()

    # Foreign keys
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey(Tenants.id, ondelete="CASCADE"))
    user_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(Users.id, ondelete="CASCADE"), unique=True
    )

    # Relationships
    embedding_models: Mapped[list[EmbeddingModels]] = relationship(
        secondary="spaces_embedding_models", order_by=EmbeddingModels.created_at
    )
    completion_models: Mapped[list[CompletionModels]] = relationship(
        secondary="spaces_completion_models", order_by=CompletionModels.created_at
    )
    members: Mapped[list["SpacesUsers"]] = relationship(
        order_by="SpacesUsers.created_at", viewonly=True
    )
    groups: Mapped[list["Groups"]] = relationship(order_by="Groups.created_at")
    assistants: Mapped[list["Assistants"]] = relationship(
        order_by="Assistants.created_at"
    )
    services: Mapped[list["Services"]] = relationship(order_by="Services.created_at")
    websites: Mapped[list["Websites"]] = relationship(order_by="Websites.created_at")
    apps: Mapped[list["Apps"]] = relationship(order_by="Apps.created_at")


class SpacesEmbeddingModels(BaseCrossReference):
    space_id: Mapped[UUID] = mapped_column(
        ForeignKey(Spaces.id, ondelete="CASCADE"), primary_key=True
    )
    embedding_model_id: Mapped[UUID] = mapped_column(
        ForeignKey(EmbeddingModels.id, ondelete="CASCADE"), primary_key=True
    )


class SpacesCompletionModels(BaseCrossReference):
    space_id: Mapped[UUID] = mapped_column(
        ForeignKey(Spaces.id, ondelete="CASCADE"), primary_key=True
    )
    completion_model_id: Mapped[UUID] = mapped_column(
        ForeignKey(CompletionModels.id, ondelete="CASCADE"), primary_key=True
    )


class SpacesUsers(BaseCrossReference):
    space_id: Mapped[UUID] = mapped_column(
        ForeignKey(Spaces.id, ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(Users.id, ondelete="CASCADE"), primary_key=True
    )
    role: Mapped[str] = mapped_column()

    # Relationships
    user: Mapped["Users"] = relationship()
