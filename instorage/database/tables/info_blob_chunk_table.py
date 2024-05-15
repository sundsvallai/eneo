from uuid import UUID

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from instorage.database.tables.base_class import BaseUuidPk
from instorage.database.tables.info_blobs_table import InfoBlobs


class InfoBlobChunks(BaseUuidPk):
    text: Mapped[str] = mapped_column()
    chunk_no: Mapped[int] = mapped_column()
    embedding: Mapped[list[float]] = mapped_column(Vector)

    # Foreign keys
    info_blob_id: Mapped[UUID] = mapped_column(
        ForeignKey(InfoBlobs.uuid, ondelete="CASCADE")
    )
    info_blob_old_id: Mapped[str] = mapped_column()
