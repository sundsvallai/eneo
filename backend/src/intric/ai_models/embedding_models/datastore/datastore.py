import time
from typing import Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic_settings import BaseSettings

from intric.ai_models.completion_models.context_builder import count_tokens
from intric.ai_models.embedding_models.embedding_model_adapters.base import (
    EmbeddingModelAdapter,
)
from intric.files.chunk_embedding_list import ChunkEmbeddingList
from intric.groups.api.group_models import Group
from intric.info_blobs.info_blob import (
    InfoBlobChunk,
    InfoBlobChunkInDBWithScore,
    InfoBlobChunkWithEmbedding,
    InfoBlobInDB,
)
from intric.info_blobs.info_blob_chunk_repo import InfoBlobChunkRepo
from intric.main.logging import get_logger
from intric.users.user import UserInDB
from intric.websites.website_models import Website

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
        user: UserInDB,
        info_blob_chunk_repo: InfoBlobChunkRepo,
        embedding_model_adapter: EmbeddingModelAdapter,
    ):
        self.user = user
        self.chunk_repo = info_blob_chunk_repo
        self.model_adapter = embedding_model_adapter

    def _chunk_text(self, info_blob: InfoBlobInDB):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=count_tokens,
        )

        info_blob_chunks = [
            InfoBlobChunk(
                chunk_no=i,
                text=chunk.strip(),
                info_blob_id=info_blob.id,
                tenant_id=self.user.tenant_id,
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
                InfoBlobChunkWithEmbedding(
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
                f"Info Blob {info_blob.id} did not yield any chunks after splitting."
            )
            return

        logger.debug(f"Embedding {len(info_blob_chunks)} info-blob chunks.")
        chunk_embedding_list = await self.model_adapter.get_embeddings(info_blob_chunks)

        logger.debug(f"Adding {len(info_blob_chunks)} info-blob chunks to datastore.")
        await self._add(chunk_embedding_list)

    async def semantic_search(
        self,
        search_string: str,
        groups: list[Group] = [],
        websites: list[Website] = [],
        num_chunks: Optional[int] = 30,
        autocut_cutoff: Optional[int] = None,
    ) -> list[InfoBlobChunkInDBWithScore]:
        group_ids = [group.id for group in groups]
        website_ids = [website.id for website in websites]

        start = time.time()
        search_string_embedding = await self.model_adapter.get_embedding_for_query(
            search_string
        )
        step_1 = time.time()
        semantic_results = await self.chunk_repo.semantic_search(
            search_string_embedding,
            group_ids=group_ids,
            website_ids=website_ids,
            limit=num_chunks,
        )
        end = time.time()

        logger.debug(
            f"Time to get results: Embed step: {step_1 - start},"
            f" Search step: {end - step_1}, Total: {end - start}"
        )

        scores = [res.score for res in semantic_results]

        if autocut_cutoff is not None:
            cut_point = autocut(scores, autocut_cutoff)
            return semantic_results[:cut_point]

        return semantic_results
