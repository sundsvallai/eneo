import openai
from tenacity import (
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from instorage.ai_models.embedding_models.embedding_model import EmbeddingModel
from instorage.ai_models.embedding_models.embedding_model_adapters.base import (
    EmbeddingModelAdapter,
)
from instorage.files.chunk_embedding_list import ChunkEmbeddingList
from instorage.info_blobs.info_blob import InfoBlobChunk
from instorage.main.config import get_settings
from instorage.main.exceptions import BadRequestException, OpenAIException
from instorage.main.logging import get_logger

logger = get_logger(__name__)


class OpenAIEmbeddingAdapter(EmbeddingModelAdapter):
    def __init__(
        self,
        model: EmbeddingModel,
        client=openai.AsyncOpenAI(api_key=get_settings().openai_api_key),
    ):
        self.client = client
        self.model_name = model.name  # Store the model name
        super().__init__(model)

    def _chunk_chunks(self, chunks: list[InfoBlobChunk]):
        cum_len = 0
        prev_i = 0
        for i, text in enumerate(chunks):
            cum_len += len(text.text)

            if cum_len > self.model.max_input:
                yield chunks[prev_i:i]
                prev_i = i
                cum_len = 0

        yield chunks[prev_i:]

    async def get_embeddings(self, chunks: list[InfoBlobChunk]):
        chunk_embedding_list = ChunkEmbeddingList()
        for chunked_chunks in self._chunk_chunks(chunks):
            texts_for_chunks = [chunk.text for chunk in chunked_chunks]

            logger.debug(f"Embedding a chunk of {len(chunked_chunks)} chunks")

            embeddings_for_chunks = await self._get_embeddings(texts=texts_for_chunks)
            chunk_embedding_list.add(chunked_chunks, embeddings_for_chunks)

        return chunk_embedding_list

    async def get_embedding_for_query(self, query: str):
        truncated_query = query[: self.model.max_input]
        embeddings = await self._get_embeddings([truncated_query])
        return embeddings[0]

    @retry(
        wait=wait_random_exponential(min=1, max=20),
        stop=stop_after_attempt(3),
        retry=retry_if_not_exception_type(BadRequestException),
        reraise=True,
    )
    async def _get_embeddings(self, texts: list[str]):
        try:
            # Prepare the parameters for the embeddings.create method
            params = {"input": texts, "model": self.model_name}

            # If dimensions exists on the model, add it to the parameters
            if self.model.dimensions is not None:
                params["dimensions"] = self.model.dimensions

            # Call the OpenAI API to get the embeddings
            response = await self.client.embeddings.create(**params)

        except openai.BadRequestError as e:
            logger.exception("Bad request error:")
            raise BadRequestException("Invalid input") from e
        except openai.RateLimitError as e:
            logger.exception("Rate limit error:")
            raise OpenAIException("OpenAI Ratelimit exception") from e
        except Exception as e:
            logger.exception("Unknown OpenAI exception:")
            raise OpenAIException("Unknown OpenAI exception") from e

        return [embedding.embedding for embedding in response.data]
