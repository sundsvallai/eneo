from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from instorage.database.tables.base_class import BaseUuidPk
from instorage.database.tables.tenant_table import Tenants
from instorage.database.tables.users_table import Users
from instorage_prop.crawler.crawl_models import CrawlType


class Crawls(BaseUuidPk):
    name: Mapped[Optional[str]] = mapped_column()
    url: Mapped[str] = mapped_column()
    allowed_path: Mapped[Optional[str]] = mapped_column()
    download_files: Mapped[bool] = mapped_column()
    crawl_type: Mapped[CrawlType] = mapped_column()

    # Foreign keys
    tenant_id: Mapped[UUID] = mapped_column(
        ForeignKey(Tenants.uuid, ondelete="CASCADE"),
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(Users.uuid, ondelete="CASCADE"),
    )
