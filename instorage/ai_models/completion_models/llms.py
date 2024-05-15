from enum import Enum
from functools import lru_cache
from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict
from pydantic.networks import HttpUrl

from instorage.logging.logging import LoggingDetails


class CompletionModelName(str, Enum):
    CHATGPT = "ChatGPT"
    GPT_4 = "GPT-4"
    MIXTRAL = "Mixtral"
    OPENSOURCE = "Open source"


class ModelFamily(str, Enum):
    OPEN_AI = "openai"
    MISTRAL = "mistral"
    VLLM = "vllm"


class ModelString(str, Enum):
    GPT_3_TURBO = "gpt-3.5-turbo"
    GPT_4_TURBO = "gpt-4-turbo"

    # Legacy models
    QWEN = "Qwen/Qwen1.5-14B-Chat"
    GPT_3_TURBO_16K = "gpt-3.5-turbo-16k"
    GPT_4 = "gpt-4"
    MIXTRAL_7X7B = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    GPT_4_PREVIEW = "gpt-4-turbo-preview"


class ModelStability(str, Enum):
    STABLE = "stable"
    EXPERIMENTAL = "experimental"


class ModelHostingLocation(str, Enum):
    USA = "usa"
    EU = "eu"


class CompletionModel(BaseModel):
    name: CompletionModelName
    nickname: str
    family: ModelFamily
    token_limit: int
    selectable: bool = True
    nr_billion_parameters: Optional[int] = None
    hf_link: Optional[HttpUrl] = None
    stability: ModelStability = ModelStability.STABLE
    hosting: ModelHostingLocation = ModelHostingLocation.USA
    can_access: bool = True


class CompletionModelResponse(BaseModel):
    completion: Union[str, Any]  # Pydantic doesn't support AsyncIterable
    model: ModelString
    extended_logging: Optional[LoggingDetails] = None


class QueryTokenCounts(BaseModel):
    question: int
    model_prompt: int
    previous_questions: list[int]
    document_chunks: list[int]

    model_config = ConfigDict(protected_namespaces=())


FROM_DOMAIN = {
    ModelString.GPT_3_TURBO: CompletionModelName.CHATGPT,
    ModelString.GPT_4_TURBO: CompletionModelName.GPT_4,
    # Legacy models
    ModelString.QWEN: CompletionModelName.OPENSOURCE,
    ModelString.GPT_4_PREVIEW: CompletionModelName.GPT_4,
    ModelString.MIXTRAL_7X7B: CompletionModelName.MIXTRAL,
    ModelString.GPT_3_TURBO_16K: CompletionModelName.CHATGPT,
    ModelString.GPT_4: CompletionModelName.GPT_4,
}


def supported_models():
    return [
        CompletionModel(
            name=CompletionModelName.GPT_4,
            nickname=CompletionModelName.GPT_4,
            family=ModelFamily.OPEN_AI,
            token_limit=128000,
        ),
        CompletionModel(
            name=CompletionModelName.CHATGPT,
            nickname=CompletionModelName.CHATGPT,
            family=ModelFamily.OPEN_AI,
            token_limit=16385,
        ),
        CompletionModel(
            name=CompletionModelName.MIXTRAL,
            nickname=CompletionModelName.MIXTRAL,
            family=ModelFamily.MISTRAL,
            token_limit=16384,
            selectable=False,
            stability=ModelStability.EXPERIMENTAL,
            hosting=ModelHostingLocation.EU,
        ),
        CompletionModel(
            name=CompletionModelName.OPENSOURCE,
            nickname="Qwen",
            family=ModelFamily.VLLM,
            token_limit=32000,  # Change this one when changing the open source model
            nr_billion_parameters=14,
            hf_link="https://huggingface.co/Qwen/Qwen1.5-14B-Chat",
            stability=ModelStability.EXPERIMENTAL,
            hosting=ModelHostingLocation.EU,
            selectable=False,
        ),
    ]


@lru_cache
def model_string_to_model():
    return {model.name: model for model in supported_models()}


def get_completion_model(model_name: str) -> CompletionModel:
    return model_string_to_model().get(model_name, None)
