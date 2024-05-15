from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from instorage.database.tables.base_class import BasePublic
from instorage.database.tables.tenant_table import Tenants

if TYPE_CHECKING:
    from instorage.database.tables.assistant_table import Assistants
    from instorage.database.tables.groups_table import Groups
    from instorage.database.tables.service_table import Services
    from instorage.database.tables.users_table import Users


class UserGroups(BasePublic):
    name: Mapped[str] = mapped_column()
    tenant_id: Mapped[int] = mapped_column(ForeignKey(Tenants.id, ondelete="CASCADE"))

    # relationships
    tenant: Mapped[Tenants] = relationship()
    users: Mapped[list["Users"]] = relationship(secondary="usergroups_users")
    assistants: Mapped[list["Assistants"]] = relationship(
        secondary="usergroups_assistants"
    )
    services: Mapped[list["Services"]] = relationship(secondary="usergroups_services")
    groups: Mapped[list["Groups"]] = relationship(secondary="usergroups_groups")

    __table_args__ = (
        UniqueConstraint("name", "tenant_id", name="user_groups_name_tenant_unique"),
    )
