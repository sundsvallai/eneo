from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from instorage.database.tables.base_class import Base, BasePublic
from instorage.database.tables.tenant_table import Tenants
from instorage.database.tables.user_groups_table import UserGroups
from instorage.database.tables.users_table import Users


class Groups(BasePublic):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(nullable=False)
    is_public: Mapped[bool] = mapped_column(nullable=False)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey(Tenants.id, ondelete="CASCADE"), index=True, nullable=False
    )
    embedding_model: Mapped[str] = mapped_column()
    index_type: Mapped[str] = mapped_column()

    # relationships
    user: Mapped[Users] = relationship()
    user_groups: Mapped[list[UserGroups]] = relationship(
        secondary="usergroups_groups", viewonly=True
    )


usergroups_groups_table = Table(
    "usergroups_groups",
    Base.metadata,
    Column("group_id", ForeignKey(Groups.id, ondelete="CASCADE"), primary_key=True),
    Column(
        "user_group_id", ForeignKey(UserGroups.id, ondelete="CASCADE"), primary_key=True
    ),
)
