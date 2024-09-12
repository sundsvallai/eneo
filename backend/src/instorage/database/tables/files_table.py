from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column

from instorage.database.tables.base_class import BasePublic
from instorage.database.tables.tenant_table import Tenants
from instorage.database.tables.users_table import Users
from instorage.files.file_models import FileType


class Files(BasePublic):
    name: Mapped[str] = mapped_column()
    text: Mapped[Optional[str]] = mapped_column()
    image: Mapped[Optional[str]] = mapped_column(BYTEA)
    checksum: Mapped[str] = mapped_column(index=True)
    size: Mapped[int] = mapped_column()
    mimetype: Mapped[Optional[str]] = mapped_column()
    file_type: Mapped[str] = mapped_column(server_default=FileType.TEXT)

    # Foreign keys
    user_id: Mapped[UUID] = mapped_column(ForeignKey(Users.id, ondelete="CASCADE"))
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey(Tenants.id, ondelete="CASCADE"))
