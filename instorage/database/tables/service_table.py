from sqlalchemy import Column, ForeignKey, Table, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, relationship

from instorage.database.tables.assistant_table import Agents
from instorage.database.tables.base_class import Base
from instorage.database.tables.user_groups_table import UserGroups


class Services(Agents):
    __tablename__ = None

    output_format = Column(Text)
    json_schema = Column(JSONB)

    # relationships
    user_groups: Mapped[list[UserGroups]] = relationship(
        secondary="usergroups_services", viewonly=True
    )

    __mapper_args__ = {"polymorphic_identity": "service"}


usergroups_services_table = Table(
    "usergroups_services",
    Base.metadata,
    Column("service_id", ForeignKey(Services.id, ondelete="CASCADE"), primary_key=True),
    Column(
        "user_group_id", ForeignKey(UserGroups.id, ondelete="CASCADE"), primary_key=True
    ),
)
