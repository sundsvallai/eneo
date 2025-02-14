from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from intric.database.tables.ai_models_table import CompletionModels
from intric.database.tables.base_class import BasePublic


class AssistantTemplates(BasePublic):
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column()
    prompt_text: Mapped[Optional[str]] = mapped_column()
    completion_model_kwargs: Mapped[Optional[dict]] = mapped_column(JSONB)
    wizard: Mapped[Optional[dict]] = mapped_column(JSONB)
    organization: Mapped[str] = mapped_column(
        Text, server_default="default", nullable=False
    )

    completion_model_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(CompletionModels.id),
    )

    completion_model: Mapped[CompletionModels] = relationship()
