from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from instorage.database.tables.base_class import BaseWithTableName, TimestampMixin
from instorage.database.tables.groups_table import Groups
from instorage.database.tables.users_table import Users


class InfoBlobs(TimestampMixin, BaseWithTableName):
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    uuid: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        server_default=text("gen_random_uuid()"),
        unique=True,
    )
    text: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(
        ForeignKey(Users.id, ondelete="CASCADE"), index=True
    )
    title: Mapped[Optional[str]] = mapped_column()
    url: Mapped[Optional[str]] = mapped_column()
    group_id: Mapped[int] = mapped_column(
        ForeignKey(Groups.id, ondelete="CASCADE"), index=True
    )
    url: Mapped[Optional[str]] = mapped_column()
    embedding_model: Mapped[str] = mapped_column()
    size: Mapped[int] = mapped_column()

    group: Mapped[Groups] = relationship()
