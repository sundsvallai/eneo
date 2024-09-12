from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from instorage.database.tables.ai_models_table import CompletionModels
from instorage.database.tables.assistant_table import Assistants
from instorage.database.tables.base_class import BaseCrossReference, BasePublic
from instorage.database.tables.files_table import Files
from instorage.database.tables.info_blobs_table import InfoBlobs
from instorage.database.tables.logging_table import logging_table
from instorage.database.tables.service_table import Services
from instorage.database.tables.sessions_table import Sessions
from instorage.database.tables.tenant_table import Tenants


class Questions(BasePublic):
    question: Mapped[str] = mapped_column()
    answer: Mapped[str] = mapped_column()
    num_tokens_question: Mapped[int] = mapped_column()
    num_tokens_answer: Mapped[int] = mapped_column()

    # Foreign keys
    completion_model_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(CompletionModels.id, ondelete="SET NULL"),
    )
    logging_details_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(logging_table.id, ondelete="SET NULL")
    )
    session_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(Sessions.id, ondelete="CASCADE"), index=True
    )
    service_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(Services.id, ondelete="CASCADE"), index=True
    )
    tenant_id: Mapped[UUID] = mapped_column(
        ForeignKey(Tenants.id, ondelete="CASCADE"), index=True
    )

    # Relationships
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
    completion_model: Mapped[CompletionModels] = relationship()

    info_blobs: AssociationProxy[list[InfoBlobs]] = association_proxy(
        "info_blob_references", "info_blob"
    )
    files: Mapped[list[Files]] = relationship(
        secondary="questions_files", order_by=Files.created_at
    )


class InfoBlobReferences(BaseCrossReference):
    question_id: Mapped[UUID] = mapped_column(
        ForeignKey(Questions.id, ondelete="CASCADE"),
        primary_key=True,
    )
    info_blob_id: Mapped[str] = mapped_column(
        ForeignKey(InfoBlobs.id, ondelete="CASCADE"), primary_key=True
    )
    similarity_score: Mapped[Optional[float]] = mapped_column()
    info_blob: Mapped[InfoBlobs] = relationship()


class QuestionsFiles(BaseCrossReference):
    question_id: Mapped[UUID] = mapped_column(
        ForeignKey(Questions.id, ondelete="CASCADE"), primary_key=True
    )
    file_id: Mapped[UUID] = mapped_column(
        ForeignKey(Files.id, ondelete="CASCADE"), primary_key=True
    )
