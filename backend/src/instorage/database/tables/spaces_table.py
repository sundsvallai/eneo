from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from instorage.database.tables.ai_models_table import CompletionModels, EmbeddingModels
from instorage.database.tables.base_class import BaseCrossReference, BasePublic
from instorage.database.tables.tenant_table import Tenants
from instorage.database.tables.users_table import Users

if TYPE_CHECKING:
    from instorage.database.tables.assistant_table import Assistants
    from instorage.database.tables.groups_table import Groups
    from instorage.database.tables.service_table import Services
    from instorage.database.tables.websites_table import Websites


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
        order_by="SpacesUsers.created_at",
        secondary="join(Users, SpacesUsers, Users.id == SpacesUsers.user_id)",
        primaryjoin="and_(Spaces.id == SpacesUsers.space_id, Users.deleted_at == None)",
        viewonly=True,
    )
    groups: Mapped[list["Groups"]] = relationship(order_by="Groups.created_at")
    assistants: Mapped[list["Assistants"]] = relationship(
        order_by="Assistants.created_at"
    )
    services: Mapped[list["Services"]] = relationship(order_by="Services.created_at")
    websites: Mapped[list["Websites"]] = relationship(order_by="Websites.created_at")


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
