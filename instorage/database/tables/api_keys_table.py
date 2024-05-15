from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from instorage.database.tables.base_class import BaseWithTableName, TimestampMixin
from instorage.database.tables.users_table import Users


class ApiKeys(TimestampMixin, BaseWithTableName):
    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(index=True)
    truncated_key: Mapped[str] = mapped_column()
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(Users.id, ondelete="CASCADE"), unique=True
    )
    assistant_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("assistants.id", ondelete="CASCADE"), unique=True
    )
