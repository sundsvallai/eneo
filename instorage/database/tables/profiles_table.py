from sqlalchemy import Column, ForeignKey, Integer, Text

from instorage.database.tables.base_class import BaseWithTableName, TimestampMixin
from instorage.database.tables.users_table import Users


class Profiles(TimestampMixin, BaseWithTableName):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(Users.id, ondelete="CASCADE"))
    full_name = Column(Text)
    image = Column(Text)
