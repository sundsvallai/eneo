from typing import Optional

from sqlalchemy import BigInteger, Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from instorage.database.tables.base_class import Base, BasePublic
from instorage.database.tables.module_table import Modules


class Tenants(BasePublic):
    name: Mapped[str] = mapped_column(unique=True)
    display_name: Mapped[Optional[str]] = mapped_column()
    quota_limit: Mapped[int] = mapped_column(BigInteger)
    privacy_policy: Mapped[Optional[str]] = mapped_column()
    domain: Mapped[Optional[str]] = mapped_column()
    zitadel_org_id: Mapped[Optional[str]] = mapped_column()

    # relationships
    modules: Mapped[list[Modules]] = relationship(secondary="tenants_modules")


tenants_modules_table = Table(
    "tenants_modules",
    Base.metadata,
    Column("tenant_id", ForeignKey(Tenants.id, ondelete="CASCADE"), primary_key=True),
    Column("module_id", ForeignKey(Modules.id, ondelete="CASCADE"), primary_key=True),
)
