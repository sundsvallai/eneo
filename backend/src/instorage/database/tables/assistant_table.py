from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from instorage.database.tables.ai_models_table import CompletionModels
from instorage.database.tables.base_class import BaseCrossReference, BasePublic
from instorage.database.tables.groups_table import Groups
from instorage.database.tables.spaces_table import Spaces
from instorage.database.tables.users_table import Users
from instorage.database.tables.websites_table import Websites


class Assistants(BasePublic):
    name: Mapped[str] = mapped_column()
    prompt: Mapped[str] = mapped_column()
    completion_model_kwargs: Mapped[Optional[dict]] = mapped_column(JSONB)
    guardrail_active: Mapped[Optional[bool]] = mapped_column()
    logging_enabled: Mapped[bool] = mapped_column()

    space_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(Spaces.id, ondelete="CASCADE"),
    )

    # Foreign keys
    user_id: Mapped[UUID] = mapped_column(ForeignKey(Users.id, ondelete="CASCADE"))
    completion_model_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(CompletionModels.id, ondelete="SET NULL"),
    )

    # relationships
    groups: Mapped[list[Groups]] = relationship(
        secondary="assistants_groups", order_by=Groups.created_at
    )
    websites: Mapped[list[Websites]] = relationship(
        secondary="assistants_websites", order_by=Websites.created_at
    )
    user: Mapped[Users] = relationship()
    completion_model: Mapped[CompletionModels] = relationship()

    __table_args__ = {"extend_existing": True}  # Temporary


class AssistantsGroups(BaseCrossReference):
    assistant_id: Mapped[UUID] = mapped_column(
        ForeignKey(Assistants.id, ondelete="CASCADE"), primary_key=True
    )
    group_id: Mapped[UUID] = mapped_column(
        ForeignKey(Groups.id, ondelete="CASCADE"), primary_key=True
    )


class AssistantsWebsites(BaseCrossReference):
    assistant_id: Mapped[UUID] = mapped_column(
        ForeignKey(Assistants.id, ondelete="CASCADE"), primary_key=True
    )
    website_id: Mapped[UUID] = mapped_column(
        ForeignKey(Websites.id, ondelete="CASCADE"), primary_key=True
    )
