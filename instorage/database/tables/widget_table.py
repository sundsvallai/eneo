from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from instorage.database.tables.assistant_table import Assistants
from instorage.database.tables.base_class import BasePublic
from instorage.database.tables.tenant_table import Tenants
from instorage.database.tables.users_table import Users


class Widgets(BasePublic):
    name: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()
    bot_introduction: Mapped[str] = mapped_column()
    color: Mapped[str] = mapped_column()
    size: Mapped[str] = mapped_column()
    assistant_id: Mapped[int] = mapped_column(
        ForeignKey(Assistants.id, ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id, ondelete="CASCADE"))

    assistant: Mapped[Assistants] = relationship(viewonly=True)
    tenant: Mapped[Tenants] = relationship(viewonly=True, secondary="users")
