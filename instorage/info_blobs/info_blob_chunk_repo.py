from typing import Optional
from uuid import UUID

import sqlalchemy as sa
from scipy.spatial.distance import cosine

from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.groups_table import Groups
from instorage.database.tables.info_blob_chunk_table import InfoBlobChunks
from instorage.database.tables.info_blobs_table import InfoBlobs
from instorage.info_blobs.info_blob import (
    InfoBlobChunkInDB,
    InfoBlobChunkInDBWithScore,
    InfoBlobChunkWithEmbedding2,
)


class InfoBlobChunkRepo:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session=session, table=InfoBlobChunks, in_db_model=InfoBlobChunkInDB
        )

    @staticmethod
    def _filter_on_groups(stmt: sa.Select, group_ids: list[UUID]):
        return stmt.join(InfoBlobs).join(Groups).where(Groups.uuid.in_(group_ids))

    async def add(
        self, chunks: list[InfoBlobChunkWithEmbedding2]
    ) -> list[InfoBlobChunkInDB]:
        stmt = (
            sa.insert(InfoBlobChunks)
            .values([chunk.model_dump() for chunk in chunks])
            .returning(InfoBlobChunks)
        )

        return await self.delegate.get_models_from_query(stmt)

    async def delete_by_info_blob(self, info_blob_id: UUID):
        stmt = (
            sa.delete(InfoBlobChunks)
            .where(InfoBlobChunks.info_blob_id == info_blob_id)
            .returning(InfoBlobChunks)
        )

        return await self.delegate.get_models_from_query(stmt)

    async def semantic_search(
        self,
        embedding: list[float],
        *,
        group_ids: Optional[list[UUID]] = None,
        limit: int = 30,
    ) -> list[InfoBlobChunkInDBWithScore]:
        stmt = (
            sa.select(InfoBlobChunks)
            .order_by(InfoBlobChunks.embedding.cosine_distance(embedding))
            .limit(limit)
        )

        if group_ids is not None:
            stmt = self._filter_on_groups(stmt, group_ids)

        chunks_in_db = await self.delegate.get_models_from_query(stmt)

        chunks_with_score = [
            InfoBlobChunkInDBWithScore(
                **chunk.model_dump(), score=1 - cosine(chunk.embedding, embedding)
            )
            for chunk in chunks_in_db
        ]

        return chunks_with_score

    async def keyword_search(
        self,
        search_string: str,
        *,
        group_ids: Optional[list[UUID]] = None,
        limit: int = 30,
    ):
        stmt = (
            sa.select(InfoBlobChunks)
            .filter(InfoBlobChunks.text.match(search_string))
            .limit(limit)
        )

        if group_ids is not None:
            stmt = self._filter_on_groups(stmt, group_ids)

        return await self.delegate.get_models_from_query(stmt)
