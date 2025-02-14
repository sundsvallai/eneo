from uuid import UUID

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from intric.database.tables.base_class import BasePublic
from intric.database.tables.users_table import Users
from intric.database.tables.tenant_table import Tenants


class Integration(BasePublic):
    __tablename__ = "integrations"

    name: Mapped[str] = mapped_column(Text, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)


class TenantIntegration(BasePublic):
    __tablename__ = "tenant_integrations"

    tenant_id: Mapped[UUID] = mapped_column(ForeignKey(Tenants.id, ondelete="CASCADE"))
    integration_id: Mapped[UUID] = mapped_column(
        ForeignKey(Integration.id, ondelete="CASCADE")
    )
    enabled: Mapped[bool] = mapped_column(server_default="False", nullable=False)

    integration: Mapped[Integration] = relationship()


class UserIntegration(BasePublic):
    __tablename__ = "user_integrations"

    user_id: Mapped[UUID] = mapped_column(ForeignKey(Users.id, ondelete="CASCADE"))
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey(Tenants.id, ondelete="CASCADE"))
    tenant_integration_id: Mapped[UUID] = mapped_column(
        ForeignKey(TenantIntegration.id, ondelete="CASCADE")
    )
    authenticated: Mapped[bool] = mapped_column(server_default="False", nullable=False)

    tenant_integration: Mapped[TenantIntegration] = relationship()
