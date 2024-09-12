from sqlalchemy.orm import Mapped, mapped_column

from instorage.database.tables.base_class import BasePublic


class Modules(BasePublic):
    name: Mapped[str] = mapped_column(unique=True)
