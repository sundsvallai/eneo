from instorage.ai_models.completion_models.completion_model_adapters.base import (  # noqa
    ModelAdapterBase,
)
from instorage.ai_models.completion_models.completion_model_adapters.openai_model_adapter import (  # noqa
    OpenAIModelAdapter,
)
from instorage.ai_models.completion_models.completion_model_adapters.vllm_model_adapter import (  # noqa
    VLMMModelAdapter,
)
from instorage.ai_models.completion_models.llms import (
    CompletionModel,
    CompletionModelResponse,
    ModelFamily,
    QueryTokenCounts,
)
from instorage.info_blobs.info_blob import InfoBlobChunkWithScore
from instorage.main.exceptions import QueryException, UnsupportedModelException
from instorage.main.logging import get_logger
from instorage.sessions.session import SessionInDB
from instorage.users.user import UserInDB
from instorage.users.user_service import UserService

logger = get_logger(__name__)


def weighted_generator(weight_1=1, weight_2=3):
    i = 0
    while True:
        if i % (weight_1 + weight_2) < weight_1:
            yield 1
        else:
            yield 2

        i += 1


CONTEXT_SIZE_BUFFER = 100  # Counting tokens is not an exakt science, leave some buffer


class CompletionModelService:
    def __init__(
        self,
        user_service: UserService,
        model_adapter: ModelAdapterBase,
        user: UserInDB,
    ):
        self.user_service = user_service
        self.model_adapter = model_adapter
        self.user = user
        self.max_tokens = (
            self.model_adapter.get_token_limit_of_model() - CONTEXT_SIZE_BUFFER
        )

    def _list_done(self, num_to_take, question_or_document_list):
        return num_to_take >= len(question_or_document_list)

    def _full(self, num_to_take, question_or_document_list, total_token_count):
        return (
            total_token_count + question_or_document_list[num_to_take] > self.max_tokens
        )

    def _done(
        self,
        num_blobs_to_take: int,
        num_questions_to_take: int,
        token_counts: QueryTokenCounts,
        total_token_count: int,
    ):
        if self._list_done(num_blobs_to_take, token_counts.document_chunks):
            if self._list_done(num_questions_to_take, token_counts.previous_questions):
                return True

            elif self._full(
                num_questions_to_take,
                token_counts.previous_questions,
                total_token_count,
            ):
                return True

            else:
                return False

        elif self._list_done(num_questions_to_take, token_counts.previous_questions):
            if self._full(
                num_blobs_to_take, token_counts.document_chunks, total_token_count
            ):
                return True
            else:
                return False

        elif self._full(
            num_questions_to_take, token_counts.previous_questions, total_token_count
        ):
            if self._full(
                num_blobs_to_take, token_counts.document_chunks, total_token_count
            ):
                return True
            else:
                return False

        return False

    def _get_number_of_each_to_add(
        self, token_counts: QueryTokenCounts, current_token_count: int
    ):
        num_blobs_to_take = 0
        num_questions_to_take = 0

        gen = weighted_generator()

        while True:
            if self._done(
                num_blobs_to_take,
                num_questions_to_take,
                token_counts,
                current_token_count,
            ):
                break

            next_to_take = next(gen)

            if next_to_take == 1:
                if num_questions_to_take >= len(token_counts.previous_questions) or (
                    current_token_count
                    + token_counts.previous_questions[num_questions_to_take]
                    > self.max_tokens
                ):
                    continue

                current_token_count += token_counts.previous_questions[
                    num_questions_to_take
                ]
                num_questions_to_take += 1

            elif next_to_take == 2:
                if num_blobs_to_take >= len(token_counts.document_chunks) or (
                    current_token_count
                    + token_counts.document_chunks[num_blobs_to_take]
                    > self.max_tokens
                ):
                    continue

                current_token_count += token_counts.document_chunks[num_blobs_to_take]
                num_blobs_to_take += 1

        return num_questions_to_take, num_blobs_to_take, current_token_count

    def _create_query(
        self,
        input_str: str,
        prompt: str = None,
        info_blobs: list[InfoBlobChunkWithScore] = [],
        session: SessionInDB | None = None,
    ):
        previous_questions = session.questions if session is not None else []

        self.model_adapter.setup(
            input=input_str,
            prompt=prompt,
            document_chunks=info_blobs,
            previous_questions=previous_questions,
        )

        token_counts = self.model_adapter.get_token_counts()

        current_token_count = token_counts.model_prompt + token_counts.question

        if current_token_count > self.max_tokens:
            logger.warning(
                f"Query too long: {current_token_count} > {self.max_tokens}. Token"
                f" usage: {token_counts}"
            )
            raise QueryException("Query too long")

        qs_to_add, is_to_add, total_token_count = self._get_number_of_each_to_add(
            token_counts=token_counts, current_token_count=current_token_count
        )

        self.model_adapter.create_query(num_questions=qs_to_add, num_docs=is_to_add)

        logger.info(f"Sending: Questions: {qs_to_add}, info-blobs: {is_to_add}")

        return total_token_count

    async def get_response(
        self,
        question: str,
        prompt: str = None,
        info_blobs: list[InfoBlobChunkWithScore] = [],
        session: SessionInDB | None = None,
        stream: bool = False,
        extended_logging: bool = False,
    ):
        total_token_count = self._create_query(question, prompt, info_blobs, session)
        await self.user_service.update_used_tokens(self.user.id, total_token_count)

        if extended_logging:
            logging_details = self.model_adapter.get_logging_details()
        else:
            logging_details = None

        if not stream:
            completion = await self.model_adapter.get_response()
        else:
            # Will be an async generator - not awaitable
            completion = self.model_adapter.get_response_streaming()

        return CompletionModelResponse(
            completion=completion,
            model=self.model_adapter.get_real_model_string(),
            extended_logging=logging_details,
        )


class CompletionModelServiceFactory:
    @classmethod
    async def create(
        cls,
        model: CompletionModel,
        model_kwargs: dict[str, str | float],
        user_service: UserService,
        user: UserInDB,
        with_hallucination_guard: bool = None,
        with_fairness_guard: bool = None,
    ):
        if not model.selectable:
            raise UnsupportedModelException(
                f"Completionmodel {model.name} is not supported."
            )

        match model.family:
            case ModelFamily.OPEN_AI:
                model_adapter = OpenAIModelAdapter(
                    model,
                    model_kwargs,
                    with_hallucination_guard=with_hallucination_guard,
                    with_fairness_guard=with_fairness_guard,
                )

            case ModelFamily.VLLM:
                model_adapter = VLMMModelAdapter(
                    model,
                    model_kwargs,
                    with_hallucination_guard=with_hallucination_guard,
                    with_fairness_guard=with_fairness_guard,
                )

            case _:
                raise NotImplementedError

        return CompletionModelService(
            user_service=user_service,
            user=user,
            model_adapter=model_adapter,
        )
