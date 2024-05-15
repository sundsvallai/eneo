import json
from enum import Enum

import tiktoken
from openai import AsyncOpenAI

from instorage.ai_models.completion_models import get_response_open_ai
from instorage.ai_models.completion_models.completion_model_adapters.base import (
    ModelAdapterBase,
)
from instorage.ai_models.completion_models.llms import (
    CompletionModel,
    CompletionModelName,
    ModelString,
    QueryTokenCounts,
)
from instorage.logging.logging import LoggingDetails
from instorage.main.config import get_settings
from instorage.main.logging import get_logger

logger = get_logger(__name__)


class OpenAIModels(str, Enum):
    GPT_3_TURBO = ModelString.GPT_3_TURBO.value
    GPT_4_TURBO = ModelString.GPT_4_TURBO.value


TOKENS_RESERVED_FOR_COMPLETION = 1000
DISALLOWED_MODEL_KWARGS = ["stream", "model", "messages"]

# Map in-domain models to Open AI models
FROM_DOMAIN_MAP = {
    CompletionModelName.CHATGPT: OpenAIModels.GPT_3_TURBO,
    CompletionModelName.GPT_4: OpenAIModels.GPT_4_TURBO,
}


class OpenAIModelAdapter(ModelAdapterBase):
    def __init__(
        self,
        model: CompletionModel,
        model_kwargs: dict[str, str | float] = {},
        client: AsyncOpenAI = AsyncOpenAI(api_key=get_settings().openai_api_key),
        with_hallucination_guard: bool = None,
        with_fairness_guard: bool = None,
    ):
        self.client = client
        self.openai_model_name = FROM_DOMAIN_MAP[model.name]

        super().__init__(
            model,
            model_kwargs,
            with_hallucination_guard=with_hallucination_guard,
            with_fairness_guard=with_fairness_guard,
        )
        self.model_kwargs = self._get_allowed_model_kwargs(model_kwargs)

    def _get_allowed_model_kwargs(self, model_kwargs: dict[str, str | float]):
        for key in DISALLOWED_MODEL_KWARGS:
            model_kwargs.pop(key, None)

        return model_kwargs

    def get_real_model_string(self) -> str:
        return self.openai_model_name

    def get_logging_details(self):
        assert self._query is not None

        return LoggingDetails(
            json_body=json.dumps(self._query), model_kwargs=self.model_kwargs
        )

    def get_token_limit_of_model(self):
        return self.model.token_limit - TOKENS_RESERVED_FOR_COMPLETION

    def get_token_counts(self):
        try:
            encoding = tiktoken.encoding_for_model(self.openai_model_name)
        except KeyError:
            # Default
            logger.warning(f"Using default encoding for model {self.openai_model_name}")
            encoding = tiktoken.get_encoding("cl100k_base")

        tokens_per_message = 3

        question_token_len = (
            len(encoding.encode(self._delegate.get_input())) + 3
        )  # every reply is primed with <|start|>assistant<|message|>

        model_prompt_token_len = (
            len(encoding.encode(self._delegate.get_prompt())) + tokens_per_message
        )

        questions_token_len = [
            len(encoding.encode(q.question))
            + tokens_per_message
            + len(encoding.encode(q.answer))
            + tokens_per_message
            for q in self._delegate.get_previous_questions()
        ]

        doc_chunks_token_len = [
            len(encoding.encode(chunk))
            for chunk in self._delegate.get_document_chunks_list()
        ]

        return QueryTokenCounts(
            question=question_token_len,
            model_prompt=model_prompt_token_len,
            previous_questions=questions_token_len,
            document_chunks=doc_chunks_token_len,
        )

    def create_query(self, num_docs: int = None, num_questions: int = None):
        prompt = self._delegate.get_prompt()
        background_info = self._delegate.get_background_info(num_docs)

        system_information = prompt

        if background_info:
            system_information = f"{system_information}\n\n{background_info}"

        system_message = [{"role": "system", "content": system_information}]

        conversation_history = [
            message
            for question in self._delegate.get_previous_questions(num_questions)
            for message in [
                {"role": "user", "content": question.question},
                {"role": "assistant", "content": question.answer},
            ]
        ]

        question = [{"role": "user", "content": self._delegate.get_input()}]

        self._query = system_message + conversation_history + question

    async def get_response(self):
        return await get_response_open_ai.get_response(
            client=self.client,
            model_name=self.openai_model_name,
            messages=self._query,
            model_kwargs=self.model_kwargs,
        )

    def get_response_streaming(self):
        return get_response_open_ai.get_response_streaming(
            client=self.client,
            model_name=self.openai_model_name,
            messages=self._query,
            model_kwargs=self.model_kwargs,
        )
