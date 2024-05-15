import time
from typing import Optional

import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic_settings import BaseSettings

from instorage.ai_models.embedding_models.embedding_model_adapters.base import (
    EmbeddingModelAdapter,
)
from instorage.groups.group import GroupInDB
from instorage.info_blobs.file.chunk_embedding_list import ChunkEmbeddingList
from instorage.info_blobs.info_blob import (
    InfoBlobChunk2,
    InfoBlobChunkWithEmbedding2,
    InfoBlobInDB,
    Query,
    QueryWithEmbedding,
)
from instorage.info_blobs.info_blob_chunk_repo import InfoBlobChunkRepo
from instorage.main.logging import get_logger

logger = get_logger(__name__)


class ChunkSettings(BaseSettings):
    chunk_size: int = 200
    chunk_overlap: int = 40


settings = ChunkSettings()


def autocut(y_values: list[float], cutoff: int = 2) -> int:
    # Written by GPT-4, fact-checked by GPT-4

    if len(y_values) <= 1:
        return len(y_values)

    # Handling division by zero in normalization
    if y_values[0] == y_values[-1]:
        return len(y_values)

    diff = []
    step = 1.0 / (len(y_values) - 1)

    for i, y in enumerate(y_values):
        x_value = float(i) * step
        y_value_norm = (y - y_values[0]) / (y_values[-1] - y_values[0])
        diff.append(y_value_norm - x_value)

    extrema_count = 0
    for i in range(1, len(diff)):
        if i == len(diff) - 1:
            if len(diff) > 2 and diff[i] > diff[i - 1] and diff[i] > diff[i - 2]:
                extrema_count += 1
                if extrema_count >= cutoff:
                    return i
        elif diff[i] > diff[i - 1] and len(diff) > i + 1 and diff[i] > diff[i + 1]:
            extrema_count += 1
            if extrema_count >= cutoff:
                return i

    return len(y_values)


class Datastore:
    def __init__(
        self,
        *,
        info_blob_chunk_repo: InfoBlobChunkRepo,
        embedding_model_adapter: EmbeddingModelAdapter,
    ):

        self.chunk_repo = info_blob_chunk_repo
        self.model_adapter = embedding_model_adapter

    def _chunk_text(self, info_blob: InfoBlobInDB):
        enc = tiktoken.get_encoding("cl100k_base")

        def length_function(text: str):
            return len(enc.encode(text))

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=length_function,
        )

        info_blob_chunks = [
            InfoBlobChunk2(
                chunk_no=i,
                text=chunk.strip(),
                info_blob_id=info_blob.uuid,
                info_blob_old_id=info_blob.id,
            )
            for i, chunk in enumerate(splitter.split_text(info_blob.text))
            if chunk.strip()
        ]

        return info_blob_chunks

    async def _add(
        self, chunk_embedding_list: ChunkEmbeddingList, batch_size: int = 100
    ):
        chunks = []
        for chunk, embedding in chunk_embedding_list:
            chunks.append(
                InfoBlobChunkWithEmbedding2(
                    **chunk.model_dump(exclude_none=True), embedding=embedding
                )
            )

            if len(chunks) >= batch_size:
                logger.debug(f"Adding {len(chunks)} chunks to datastore.")
                await self.chunk_repo.add(chunks)

                chunks.clear()

        # Last batch
        if chunks:
            logger.debug(f"Last batch. Adding {len(chunks)} chunks to datastore.")
            await self.chunk_repo.add(chunks)

    async def add(self, info_blob: InfoBlobInDB):
        logger.debug("Chunking text.")
        info_blob_chunks = self._chunk_text(info_blob)

        if not info_blob_chunks:
            logger.warning(
                f"Info Blob {info_blob.uuid} did not yield any chunks after splitting."
            )
            return

        logger.debug(f"Embedding {len(info_blob_chunks)} info-blob chunks.")
        chunk_embedding_list = await self.model_adapter.get_embeddings(info_blob_chunks)

        logger.debug(f"Adding {len(info_blob_chunks)} info-blob chunks to datastore.")
        await self._add(chunk_embedding_list)

    async def query(
        self, query: Query, groups: list[GroupInDB], embedding: list[list[float]]
    ):
        query_with_embedding = QueryWithEmbedding(
            **query.model_dump(), embedding=embedding
        )

        group_ids = [group.uuid for group in groups]

        results = await self.chunk_repo.semantic_search(
            query_with_embedding.embedding, group_ids=group_ids
        )

        return results

    async def semantic_search(
        self, search_string: str, groups: list[GroupInDB], limit: Optional[int] = 30
    ):
        group_ids = [group.uuid for group in groups]

        start = time.time()
        search_string_embedding = await self.model_adapter.get_embedding_for_query(
            search_string
        )
        step_1 = time.time()
        semantic_results = await self.chunk_repo.semantic_search(
            search_string_embedding, group_ids=group_ids, limit=limit
        )
        end = time.time()

        logger.debug(
            f"Time to get results: Embed step: {step_1 - start},"
            f" Search step: {end - step_1}, Total: {end - start}"
        )

        scores = [res.score for res in semantic_results]
        cut_point = autocut(scores, 3)

        return semantic_results[:cut_point]
