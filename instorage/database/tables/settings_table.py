from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB

from instorage.database.tables.base_class import BaseWithTableName, TimestampMixin


class Settings(TimestampMixin, BaseWithTableName):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    chatbot_widget = Column(JSONB)
