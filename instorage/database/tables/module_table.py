from sqlalchemy.orm import Mapped, mapped_column

from instorage.database.tables.base_class import BaseWithTableName, TimestampMixin


class Modules(TimestampMixin, BaseWithTableName):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
