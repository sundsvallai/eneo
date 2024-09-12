from typing import Optional
from uuid import UUID

import sqlalchemy as sa
from scipy.spatial.distance import cosine

from instorage.database.database import AsyncSession
from instorage.database.repositories.base import BaseRepositoryDelegate
from instorage.database.tables.info_blob_chunk_table import InfoBlobChunks
from instorage.database.tables.info_blobs_table import InfoBlobs
from instorage.info_blobs.info_blob import (
    InfoBlobChunkInDB,
    InfoBlobChunkInDBWithScore,
    InfoBlobChunkWithEmbedding,
)


class InfoBlobChunkRepo:
    def __init__(self, session: AsyncSession):
        self.delegate = BaseRepositoryDelegate(
            session=session, table=InfoBlobChunks, in_db_model=InfoBlobChunkInDB
        )
        self.session = session

    @staticmethod
    def _filter_on_groups_and_websites(
        stmt: sa.Select, group_ids: list[UUID], website_ids: list[UUID]
    ):
        return stmt.join(InfoBlobs).where(
            sa.or_(
                InfoBlobs.group_id.in_(group_ids), InfoBlobs.website_id.in_(website_ids)
            )
        )

    async def add(
        self, chunks: list[InfoBlobChunkWithEmbedding]
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
        group_ids: Optional[list[UUID]] = [],
        website_ids: Optional[list[UUID]] = [],
        limit: int = 30,
    ) -> list[InfoBlobChunkInDBWithScore]:
        # Postgres will sometimes think that a sequential scan of the whole table is
        # preferable to an index scan, when it is not. This is because this particular
        # table has a lot of data in TOAST tables, which postgres apparently fails
        # to account for when planning the query.
        #
        # The solution below is a crude one, and we should revisit this at some point
        # in the future. This should also be the first place we look at if something
        # is slow. Note the "LOCAL", ensuring that we only punish sequential scans for
        # this particular session. This might make all future queries in this transaction
        # not be able to run sequential, but we will see if that is an issue.
        #
        # Reference: https://github.com/pgvector/pgvector/issues/662
        # TODO: Solve this issue in a more elegant way.

        await self.session.execute(sa.text("SET LOCAL enable_seqscan = off;"))

        stmt = (
            sa.select(InfoBlobChunks)
            .order_by(InfoBlobChunks.embedding.cosine_distance(embedding))
            .limit(limit)
        )

        stmt = self._filter_on_groups_and_websites(stmt, group_ids, website_ids)

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
            stmt = self._filter_on_groups_and_websites(stmt, group_ids)

        return await self.delegate.get_models_from_query(stmt)
