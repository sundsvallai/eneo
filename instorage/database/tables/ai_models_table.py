from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from instorage.ai_models.completion_models.llms import (
    ModelFamily,
    ModelHostingLocation,
    ModelStability,
)
from instorage.database.tables.base_class import BaseUuidPk


class CompletionModels(BaseUuidPk):
    name: Mapped[str] = mapped_column(unique=True)
    nickname: Mapped[str] = mapped_column()
    token_limit: Mapped[int] = mapped_column()
    selectable: Mapped[bool] = mapped_column()
    nr_billion_parameters: Mapped[Optional[int]] = mapped_column()
    hf_link: Mapped[Optional[str]] = mapped_column()

    family: Mapped[ModelFamily] = mapped_column()
    stability: Mapped[ModelStability] = mapped_column()
    hosting: Mapped[ModelHostingLocation] = mapped_column()
