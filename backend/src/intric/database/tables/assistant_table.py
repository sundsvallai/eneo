from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from intric.database.tables.ai_models_table import CompletionModels
from intric.database.tables.assistant_template_table import AssistantTemplates
from intric.database.tables.base_class import BaseCrossReference, BasePublic
from intric.database.tables.files_table import Files
from intric.database.tables.groups_table import Groups
from intric.database.tables.spaces_table import Spaces
from intric.database.tables.users_table import Users
from intric.database.tables.websites_table import Websites


class Assistants(BasePublic):
    name: Mapped[str] = mapped_column()
    completion_model_kwargs: Mapped[Optional[dict]] = mapped_column(JSONB)
    guardrail_active: Mapped[Optional[bool]] = mapped_column()
    logging_enabled: Mapped[bool] = mapped_column()
    is_default: Mapped[bool] = mapped_column()
    published: Mapped[bool] = mapped_column()

    # Foreign keys
    user_id: Mapped[UUID] = mapped_column(ForeignKey(Users.id, ondelete="CASCADE"))
    completion_model_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(CompletionModels.id),
    )
    space_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(Spaces.id, ondelete="CASCADE"),
    )
    template_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(AssistantTemplates.id, ondelete="SET NULL")
    )

    # relationships
    groups: Mapped[list[Groups]] = relationship(
        secondary="assistants_groups", order_by=Groups.created_at
    )
    websites: Mapped[list[Websites]] = relationship(
        secondary="assistants_websites", order_by=Websites.created_at
    )
    user: Mapped[Users] = relationship()
    completion_model: Mapped[Optional[CompletionModels]] = relationship()
    attachments: Mapped[list["AssistantsFiles"]] = relationship(
        order_by="AssistantsFiles.created_at", viewonly=True
    )
    template: Mapped[Optional[AssistantTemplates]] = relationship()

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


class AssistantsFiles(BaseCrossReference):
    assistant_id: Mapped[UUID] = mapped_column(
        ForeignKey(Assistants.id, ondelete="CASCADE"), primary_key=True
    )
    file_id: Mapped[UUID] = mapped_column(
        ForeignKey(Files.id, ondelete="CASCADE"), primary_key=True
    )

    # Relationships
    file: Mapped[Files] = relationship()
