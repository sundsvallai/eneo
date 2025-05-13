from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from intric.ai_models.completion_models.completion_model import (
        CompletionModel,
        Context,
        ModelKwargs,
    )


class CompletionModelAdapter(ABC):
    def __init__(self, model: "CompletionModel"):
        self.model = model

    def get_token_limit_of_model(self):
        raise NotImplementedError()

    async def get_response(self, context: "Context", model_kwargs: "ModelKwargs"):
        raise NotImplementedError()

    def get_response_streaming(self, context: "Context", model_kwargs: "ModelKwargs"):
        raise NotImplementedError()
