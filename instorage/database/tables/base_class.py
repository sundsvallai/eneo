from sqlalchemy import TIMESTAMP, Column, Integer, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    __abstract__ = True


class BaseWithTableName(Base):
    __name__: str
    __abstract__ = True

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        # Camel case to snake case
        return "".join(
            ["_" + c.lower() if c.isupper() else c for c in cls.__name__]
        ).lstrip("_")


class TimestampMixin:
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class IdMixin:
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        UUID(),
        nullable=False,
        index=True,
        server_default=text("gen_random_uuid()"),
        unique=True,
    )


class UUIDMixin:
    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )


class BasePublic(IdMixin, TimestampMixin, BaseWithTableName):
    __abstract__ = True


class BasePublicWithoutTableName(IdMixin, TimestampMixin, Base):
    __abstract__ = True


class BaseUuidPk(UUIDMixin, TimestampMixin, BaseWithTableName):
    __abstract__ = True
