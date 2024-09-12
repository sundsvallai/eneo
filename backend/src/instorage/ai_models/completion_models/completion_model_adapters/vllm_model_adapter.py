import json

import jinja2
from openai import AsyncOpenAI

from instorage.ai_models.completion_models.completion_model import (
    CompletionModel,
    Context,
    ModelKwargs,
)
from instorage.ai_models.completion_models.completion_model_adapters.openai_model_adapter import (
    OpenAIModelAdapter,
)
from instorage.logging.logging import LoggingDetails
from instorage.logging.logging_templates import LLAMA_TEMPLATE
from instorage.main.config import get_settings

JINJA_TEMPLATE = jinja2.Environment().from_string(LLAMA_TEMPLATE)


class VLMMModelAdapter(OpenAIModelAdapter):
    def __init__(
        self,
        model: CompletionModel,
        client: AsyncOpenAI = AsyncOpenAI(
            api_key="EMPTY", base_url=get_settings().vllm_model_url
        ),
    ):
        self.model = model
        self.client = client

    def get_token_limit_of_model(self):
        return self.model.token_limit

    def get_logging_details(
        self,
        context: Context,
        model_kwargs: ModelKwargs | None = None,
    ):
        query = self.create_query_from_context(context=context)
        messages = {"messages": query}
        context = JINJA_TEMPLATE.render(messages)

        return LoggingDetails(
            context=context,
            model_kwargs=self._get_kwargs(model_kwargs),
            json_body=json.dumps(query),
        )

    def create_query_from_context(self, context: Context):
        system_message = [{"role": "system", "content": context.prompt}]

        previous_messages = [
            message
            for question in context.messages
            for message in [
                {"role": "user", "content": question.question},
                {"role": "assistant", "content": question.answer},
            ]
        ]
        question = [{"role": "user", "content": context.input}]

        return system_message + previous_messages + question
