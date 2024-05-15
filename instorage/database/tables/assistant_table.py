from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from instorage.database.tables.base_class import Base, BasePublicWithoutTableName
from instorage.database.tables.groups_table import Groups
from instorage.database.tables.user_groups_table import UserGroups
from instorage.database.tables.users_table import Users

if TYPE_CHECKING:
    from instorage.database.tables.workflow_tables import Steps


class Agents(BasePublicWithoutTableName):
    __tablename__ = "assistants"

    name: Mapped[str] = mapped_column()
    prompt: Mapped[str] = mapped_column()
    completion_model: Mapped[str] = mapped_column()
    completion_model_kwargs: Mapped[Optional[dict]] = mapped_column(JSONB)
    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id, ondelete="CASCADE"))
    type: Mapped[str] = mapped_column()
    logging_enabled: Mapped[bool] = mapped_column()
    is_public: Mapped[bool] = mapped_column()

    groups: Mapped[list[Groups]] = relationship(
        secondary="agents_groups", order_by=Groups.created_at
    )
    user: Mapped[Users] = relationship()

    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "agent"}


class Assistants(Agents):
    __tablename__ = None

    guardrail_active: Mapped[Optional[bool]] = mapped_column()

    # relationships
    guard_step: Mapped["Steps"] = relationship(secondary="assistants_steps_guardrails")
    user_groups: Mapped[list[UserGroups]] = relationship(
        secondary="usergroups_assistants", viewonly=True
    )

    __mapper_args__ = {"polymorphic_identity": "assistant"}


agents_groups_table = Table(
    "agents_groups",
    Base.metadata,
    Column("agent_id", ForeignKey(Agents.id, ondelete="CASCADE"), primary_key=True),
    Column("group_id", ForeignKey(Groups.id, ondelete="CASCADE"), primary_key=True),
)

usergroups_assistants_table = Table(
    "usergroups_assistants",
    Base.metadata,
    Column(
        "assistants_id", ForeignKey(Assistants.id, ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "user_group_id", ForeignKey(UserGroups.id, ondelete="CASCADE"), primary_key=True
    ),
)
