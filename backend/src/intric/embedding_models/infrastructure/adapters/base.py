import abc
from abc import abstractmethod

from intric.embedding_models.domain.embedding_model import EmbeddingModel
from intric.files.chunk_embedding_list import ChunkEmbeddingList
from intric.info_blobs.info_blob import InfoBlobChunk


class EmbeddingModelAdapter(abc.ABC):
    def __init__(self, model: EmbeddingModel):
        self.model = model

    def _chunk_chunks(self, chunks: list["InfoBlobChunk"]):
        cum_len = 0
        prev_i = 0
        for i, chunk in enumerate(chunks):
            cum_len += len(chunk.text)

            if cum_len > self.model.max_input:
                yield chunks[prev_i:i]
                prev_i = i
                cum_len = 0

        yield chunks[prev_i:]

    @abstractmethod
    async def get_embedding_for_query(self, query: str):
        raise NotImplementedError

    @abstractmethod
    async def get_embeddings(self, chunks: list[InfoBlobChunk]) -> ChunkEmbeddingList:
        raise NotImplementedError
