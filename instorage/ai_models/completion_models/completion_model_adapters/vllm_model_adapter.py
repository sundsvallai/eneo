import json
from enum import Enum

import jinja2
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
from instorage.logging.logging_templates import QWEN_TEMPLATE

JINJA_TEMPLATE = jinja2.Environment().from_string(QWEN_TEMPLATE)


class OpenSourceModels(str, Enum):
    QWEN = ModelString.QWEN.value


# Map in-domain models to OpenSource models
FROM_DOMAIN_MAP = {CompletionModelName.OPENSOURCE: OpenSourceModels.QWEN}


class VLMMModelAdapter(ModelAdapterBase):
    def __init__(
        self,
        model: CompletionModel,
        model_kwargs: dict = {},
        client: AsyncOpenAI = AsyncOpenAI(
            api_key="EMPTY", base_url="http://65.108.33.103:8000/v1"
        ),
        with_hallucination_guard: bool = None,
        with_fairness_guard: bool = None,
    ):
        self.client = client
        self.open_source_model = FROM_DOMAIN_MAP[model.name]

        if with_fairness_guard is None:
            with_fairness_guard = True

        super().__init__(
            model,
            model_kwargs,
            with_hallucination_guard=with_hallucination_guard,
            with_fairness_guard=with_fairness_guard,
        )

    def get_real_model_string(self) -> str:
        return self.open_source_model

    async def get_response(self):
        return await get_response_open_ai.get_response(
            client=self.client,
            model_name=self.open_source_model,
            messages=self._query,
            model_kwargs=self.model_kwargs,
        )

    def get_response_streaming(self):
        return get_response_open_ai.get_response_streaming(
            client=self.client,
            model_name=self.open_source_model,
            messages=self._query,
            model_kwargs=self.model_kwargs,
        )

    def get_token_counts(self) -> QueryTokenCounts:
        encoding = tiktoken.get_encoding("cl100k_base")

        def _get_count(string):
            return len(encoding.encode(string))

        question_count = _get_count(self._delegate.get_input())
        prompt_count = _get_count(self._delegate.get_prompt())
        previous_questions_count = [
            _get_count(q.question) + _get_count(q.answer)
            for q in self._delegate.get_previous_questions()
        ]
        doc_chunks_count = [
            _get_count(chunk) for chunk in self._delegate.get_document_chunks_list()
        ]

        counts = QueryTokenCounts(
            question=question_count,
            model_prompt=prompt_count,
            previous_questions=previous_questions_count,
            document_chunks=doc_chunks_count,
        )

        return counts

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

    def get_logging_details(self):
        messages = {"messages": self._query}
        context = JINJA_TEMPLATE.render(messages)

        return LoggingDetails(
            context=context,
            model_kwargs=self.model_kwargs,
            json_body=json.dumps(self._query),
        )
