# MIT License

from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import registry

from instorage.database.tables.base_class import Base

mapper_registry = registry()


def create_logging_table(metadata_obj):
    table = Table(
        "logging",
        metadata_obj,
        Column("id", Integer, primary_key=True),
        Column("context", String),
        Column("model_kwargs", JSONB),
        Column("json_body", JSONB),
    )

    class Logging:
        pass

    mapper_registry.map_imperatively(Logging, table)

    return Logging


logging_table = create_logging_table(Base.metadata)
