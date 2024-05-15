from sqlalchemy import Boolean, Column, Integer, Text

from instorage.database.tables.base_class import BaseWithTableName, TimestampMixin


class BetaKeys(TimestampMixin, BaseWithTableName):
    id = Column(Integer, primary_key=True, index=True)
    key = Column(Text, nullable=False)
    used = Column(Boolean, nullable=False)
