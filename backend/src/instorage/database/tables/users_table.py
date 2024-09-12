from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Column, DateTime, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from instorage.database.tables.base_class import Base, BasePublic
from instorage.database.tables.roles_table import PredefinedRoles, Roles
from instorage.database.tables.tenant_table import Tenants
from instorage.database.tables.user_groups_table import UserGroups

if TYPE_CHECKING:
    from instorage.database.tables.api_keys_table import ApiKeys


class Users(BasePublic):
    username: Mapped[Optional[str]] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    email_verified: Mapped[bool] = mapped_column(server_default="False")
    salt: Mapped[Optional[str]] = mapped_column()
    password: Mapped[Optional[str]] = mapped_column()
    is_active: Mapped[bool] = mapped_column(server_default="True")
    used_tokens: Mapped[int] = mapped_column(default=0)
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey(Tenants.id, ondelete="CASCADE"))
    quota_limit: Mapped[Optional[int]] = mapped_column()
    created_with: Mapped[Optional[str]] = mapped_column()

    tenant: Mapped[Tenants] = relationship()
    api_key: Mapped["ApiKeys"] = relationship(cascade="all, delete-orphan")
    roles: Mapped[list[Roles]] = relationship(
        secondary="users_roles", order_by=Roles.created_at
    )
    predefined_roles: Mapped[list[PredefinedRoles]] = relationship(
        secondary="users_predefined_roles", order_by=PredefinedRoles.created_at
    )
    user_groups: Mapped[list[UserGroups]] = relationship(
        secondary="usergroups_users", viewonly=True
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=None
    )

    __table_args__ = (
        UniqueConstraint("username", "tenant_id", name="users_username_tenant_unique"),
    )


users_roles_table = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", ForeignKey(Users.id, ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey(Roles.id, ondelete="CASCADE"), primary_key=True),
)

users_predefined_roles_table = Table(
    "users_predefined_roles",
    Base.metadata,
    Column("user_id", ForeignKey(Users.id, ondelete="CASCADE"), primary_key=True),
    Column(
        "predefined_role_id",
        ForeignKey(PredefinedRoles.id, ondelete="CASCADE"),
        primary_key=True,
    ),
)


usergroups_users_table = Table(
    "usergroups_users",
    Base.metadata,
    Column("user_id", ForeignKey(Users.id, ondelete="CASCADE"), primary_key=True),
    Column(
        "user_group_id", ForeignKey(UserGroups.id, ondelete="CASCADE"), primary_key=True
    ),
)
