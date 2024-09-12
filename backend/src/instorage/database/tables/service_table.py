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


class Services(BasePublic):
    name: Mapped[str] = mapped_column()
    prompt: Mapped[str] = mapped_column()
    output_format: Mapped[Optional[str]] = mapped_column()
    json_schema: Mapped[Optional[dict]] = mapped_column(JSONB)
    completion_model_kwargs: Mapped[Optional[dict]] = mapped_column(JSONB)

    # Foreign keys
    user_id: Mapped[UUID] = mapped_column(ForeignKey(Users.id, ondelete="CASCADE"))
    completion_model_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(CompletionModels.id, ondelete="SET NULL"),
    )
    space_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(Spaces.id, ondelete="CASCADE"),
    )

    # relationships
    groups: Mapped[list[Groups]] = relationship(
        secondary="services_groups", order_by=Groups.created_at
    )
    user: Mapped[Users] = relationship()
    completion_model: Mapped[CompletionModels] = relationship()


class ServicesGroups(BaseCrossReference):
    service_id: Mapped[UUID] = mapped_column(
        ForeignKey(Services.id, ondelete="CASCADE"), primary_key=True
    )
    group_id: Mapped[UUID] = mapped_column(
        ForeignKey(Groups.id, ondelete="CASCADE"), primary_key=True
    )
