from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from instorage.database.tables.base_class import BasePublic
from instorage.database.tables.users_table import Users


class Jobs(BasePublic):
    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id, ondelete="CASCADE"))
    task: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()
    result_location: Mapped[Optional[str]] = mapped_column()
    name: Mapped[Optional[str]] = mapped_column()
