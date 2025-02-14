from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from intric.database.tables.ai_models_table import EmbeddingModels
from intric.database.tables.base_class import BasePublic
from intric.database.tables.groups_table import Groups
from intric.database.tables.tenant_table import Tenants
from intric.database.tables.users_table import Users
from intric.database.tables.websites_table import Websites


class InfoBlobs(BasePublic):
    text: Mapped[str] = mapped_column()
    title: Mapped[Optional[str]] = mapped_column()
    url: Mapped[Optional[str]] = mapped_column()
    size: Mapped[int] = mapped_column()

    # Foreign keys
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(Users.id, ondelete="CASCADE"), index=True
    )
    tenant_id: Mapped[UUID] = mapped_column(ForeignKey(Tenants.id, ondelete="CASCADE"))
    group_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(Groups.id, ondelete="CASCADE"), index=True
    )
    website_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(Websites.id, ondelete="CASCADE"), index=True
    )
    embedding_model_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(EmbeddingModels.id, ondelete="SET NULL"),
    )

    # relationships
    group: Mapped[Groups] = relationship()
    website: Mapped[Websites] = relationship()
    embedding_model: Mapped[Optional[EmbeddingModels]] = relationship()
