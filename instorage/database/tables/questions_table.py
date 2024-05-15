from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from instorage.database.tables.assistant_table import Assistants
from instorage.database.tables.base_class import (
    BasePublic,
    BaseWithTableName,
    TimestampMixin,
)
from instorage.database.tables.info_blobs_table import InfoBlobs
from instorage.database.tables.logging_table import logging_table
from instorage.database.tables.service_table import Services
from instorage.database.tables.sessions_table import Sessions


class Questions(BasePublic):
    session_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(Sessions.id, ondelete="CASCADE"), index=True
    )
    service_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(Services.id, ondelete="CASCADE"), index=True
    )
    question: Mapped[str] = mapped_column()
    answer: Mapped[str] = mapped_column()
    model: Mapped[Optional[str]] = mapped_column()
    logging_details_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(logging_table.id, ondelete="SET NULL")
    )

    info_blob_references: Mapped[list["InfoBlobReferences"]] = relationship(
        order_by="InfoBlobReferences.similarity_score.desc()", viewonly=True
    )
    logging_details = relationship(logging_table)
    assistant: Mapped[Assistants] = relationship(
        secondary="sessions",
        primaryjoin="Questions.session_id == Sessions.id",
        secondaryjoin="Sessions.assistant_id == Assistants.id",
        viewonly=True,
    )
    session: Mapped[Sessions] = relationship(viewonly=True)

    info_blobs: AssociationProxy[list[InfoBlobs]] = association_proxy(
        "info_blob_references", "info_blob"
    )


class InfoBlobReferences(TimestampMixin, BaseWithTableName):
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey(Questions.id, ondelete="CASCADE"),
        index=True,
    )
    info_blob_id: Mapped[str] = mapped_column(
        ForeignKey(InfoBlobs.id, ondelete="CASCADE"), index=True
    )
    similarity_score: Mapped[Optional[float]] = mapped_column()
    info_blob: Mapped[InfoBlobs] = relationship()
