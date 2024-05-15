import abc
from abc import abstractmethod

from instorage.ai_models.embedding_models.embedding_models import EmbeddingModel
from instorage.info_blobs.file.chunk_embedding_list import ChunkEmbeddingList
from instorage.info_blobs.info_blob import InfoBlobChunk


class EmbeddingModelAdapter(abc.ABC):
    def __init__(self, model: EmbeddingModel):
        self.model = model

    @abstractmethod
    async def get_embedding_for_query(self, query: str):
        raise NotImplementedError

    @abstractmethod
    async def get_embeddings(self, chunks: list[InfoBlobChunk]) -> ChunkEmbeddingList:
        raise NotImplementedError
