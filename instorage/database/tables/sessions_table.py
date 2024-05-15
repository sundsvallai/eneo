from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from instorage.database.tables.assistant_table import Assistants
from instorage.database.tables.base_class import BasePublic
from instorage.database.tables.service_table import Services
from instorage.database.tables.users_table import Users

if TYPE_CHECKING:
    from instorage.database.tables.questions_table import Questions


class Sessions(BasePublic):
    user_id: Mapped[int] = mapped_column(ForeignKey(Users.id, ondelete="CASCADE"))
    name: Mapped[str] = mapped_column()
    assistant_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(Assistants.id, ondelete="CASCADE")
    )
    service_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(Services.id, ondelete="CASCADE")
    )
    feedback_value: Mapped[Optional[int]] = mapped_column()
    feedback_text: Mapped[Optional[str]] = mapped_column()

    questions: Mapped[list["Questions"]] = relationship(order_by="Questions.created_at")
    assistant: Mapped[Optional[Assistants]] = relationship(
        foreign_keys="Sessions.assistant_id", viewonly=True
    )
