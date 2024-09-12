from typing import Optional

import tiktoken

from instorage.ai_models.completion_models.completion_model import (
    CompletionModel,
    CompletionModelResponse,
    Context,
    Message,
    ModelKwargs,
)
from instorage.ai_models.completion_models.completion_model_adapters.claude_model_adapter import (
    ClaudeModelAdapter,
)
from instorage.ai_models.completion_models.completion_model_adapters.openai_model_adapter import (  # noqa
    OpenAIModelAdapter,
)
from instorage.ai_models.completion_models.context_builder import ContextBuilder
from instorage.files.file_models import File, FileType
from instorage.info_blobs.info_blob import InfoBlobChunkInDBWithScore
from instorage.main.exceptions import BadRequestException, QueryException
from instorage.main.logging import get_logger
from instorage.questions.question import Question
from instorage.sessions.session import SessionInDB
from instorage.users.user import UserInDB
from instorage.users.user_service import UserService

logger = get_logger(__name__)


CONTEXT_SIZE_BUFFER = 300  # Counting tokens is not an exakt science, leave some buffer


def count_tokens(text: str):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


class CompletionService:
    def __init__(
        self,
        user_service: UserService,
        model_adapter: OpenAIModelAdapter | ClaudeModelAdapter,
        user: UserInDB,
        context_builder: ContextBuilder,
    ):
        self.user_service = user_service
        self.model_adapter = model_adapter
        self.user = user
        self.context_builder = context_builder

    def _get_max_tokens(self):
        return self.model_adapter.get_token_limit_of_model() - CONTEXT_SIZE_BUFFER

    def _count_tokens_of_context(self, context: Context):
        prompt_len = count_tokens(context.prompt)
        input_question_len = count_tokens(context.input)

        return prompt_len + input_question_len

    def _count_tokens_of_previous_messages(self, previous_messages: list[Question]):
        return sum(
            count_tokens(text)
            for message in previous_messages
            for text in [message.question, message.answer]
        )

    def get_number_of_questions(
        self, max_tokens: int, question_counts: list[int], start_count: int = 0
    ):
        # Count from the end (most recent questions)
        cur_count = start_count
        for i, count in enumerate(reversed(question_counts)):
            cur_count += count
            if cur_count > max_tokens:
                return i

        return len(question_counts)

    def _check_completion_model_vision(
        self,
        completion_model: CompletionModel,
        files: list[File],
    ):
        if any([file.file_type == FileType.IMAGE for file in files]):
            if not completion_model.vision:
                raise BadRequestException(
                    f"Completion model {completion_model.name} do not support vision."
                )

    def get_context(
        self,
        max_tokens: int,
        input_str: str,
        files: list[File] = [],
        prompt: str = "",
        info_blobs_chunks: list[InfoBlobChunkInDBWithScore] = [],
        session: Optional[SessionInDB] = None,
    ):
        if files:
            self._check_completion_model_vision(
                completion_model=self.model_adapter.model,
                files=files,
            )

        # Set hallucination guard only if there are info_blob_chunks
        hallucination_guard = bool(info_blobs_chunks)

        context = self.context_builder.build_context(
            input=input_str,
            files=files,
            prompt=prompt,
            session=session,
            info_blob_chunks=info_blobs_chunks,
            hallucination_guard=hallucination_guard,
        )

        token_count = self._count_tokens_of_context(context)
        if token_count > max_tokens:
            logger.warning(f"Query too long: {token_count} > {max_tokens}.")
            raise QueryException("Query too long")

        context.token_count = token_count

        return context

    def get_messages(self, messages: list[Message], token_count: int, max_tokens: int):
        question_counts = [
            count_tokens(message.question) + count_tokens(message.answer)
            for message in messages
        ]
        num_questions = self.get_number_of_questions(
            max_tokens, question_counts, start_count=token_count
        )

        return messages[-num_questions:]

    async def get_response(
        self,
        question: str,
        model_kwargs: ModelKwargs | None = None,
        files: list[File] = [],
        prompt: str = "",
        info_blob_chunks: list[InfoBlobChunkInDBWithScore] = [],
        session: SessionInDB | None = None,
        stream: bool = False,
        extended_logging: bool = False,
    ):
        # Make sure everything fits in the context of the model
        max_tokens = self._get_max_tokens()
        context = self.get_context(
            max_tokens,
            question,
            files,
            prompt=prompt,
            session=session,
            info_blobs_chunks=info_blob_chunks,
        )
        context.messages = self.get_messages(
            messages=context.messages,
            token_count=context.token_count,
            max_tokens=max_tokens,
        )

        # Update token count
        # TODO: Remove this when we save tokens on a question level
        total_token_count = (
            context.token_count
            + self._count_tokens_of_previous_messages(context.messages)
        )
        await self.user_service.update_used_tokens(self.user.id, total_token_count)

        if extended_logging:
            logging_details = self.model_adapter.get_logging_details(
                context=context, model_kwargs=model_kwargs
            )
        else:
            logging_details = None

        if not stream:
            completion = await self.model_adapter.get_response(
                context=context,
                model_kwargs=model_kwargs,
            )
        else:
            # Will be an async generator - not awaitable
            completion = self.model_adapter.get_response_streaming(
                context=context,
                model_kwargs=model_kwargs,
            )

        return CompletionModelResponse(
            completion=completion,
            model=self.model_adapter.model,
            extended_logging=logging_details,
            total_token_count=total_token_count,
        )
