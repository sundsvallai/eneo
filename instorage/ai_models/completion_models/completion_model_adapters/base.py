import abc
from abc import abstractmethod

from instorage.ai_models.completion_models.context_builder import ContextBuilder
from instorage.ai_models.completion_models.llms import CompletionModel, QueryTokenCounts
from instorage.info_blobs.info_blob import InfoBlobChunkWithScore
from instorage.main.logging import get_logger
from instorage.questions.question import QuestionInDB

logger = get_logger(__name__)


class ModelAdapterBase(abc.ABC):
    def __init__(
        self,
        model: CompletionModel,
        model_kwargs: dict = {},
        with_hallucination_guard: bool = None,
        with_fairness_guard: bool = None,
    ):
        self.model = model
        self.model_kwargs = model_kwargs

        self._delegate = ContextBuilder(
            with_hallucination_guard=with_hallucination_guard,
            with_fairness_guard=with_fairness_guard,
        )

        self._query = None

    def setup(
        self,
        *,
        input: str,
        prompt: str = None,
        document_chunks: list[InfoBlobChunkWithScore] = None,
        previous_questions: list[QuestionInDB] = None,
    ):
        self._delegate.setup(
            input=input,
            prompt=prompt,
            document_chunks=document_chunks,
            previous_questions=previous_questions,
        )

    def get_query(self):
        if self._query is None:
            logger.warning("Query not created yet!")

        else:
            return self._query

    def get_token_limit_of_model(self):
        return self.model.token_limit

    @abstractmethod
    def get_logging_details(self):
        raise NotImplementedError

    @abstractmethod
    def create_query(self, num_docs: int = None, num_questions: int = None):
        raise NotImplementedError

    @abstractmethod
    def get_token_counts(self) -> QueryTokenCounts:
        raise NotImplementedError

    @abstractmethod
    async def get_response(self):
        raise NotImplementedError

    @abstractmethod
    async def get_response_streaming(self):
        raise NotImplementedError

    @abstractmethod
    def get_real_model_string(self) -> str:
        raise NotImplementedError
