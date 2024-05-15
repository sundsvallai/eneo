from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic import BaseModel
from pydantic.networks import HttpUrl

from instorage.ai_models.completion_models.llms import (
    ModelHostingLocation,
    ModelStability,
)


class EmbeddingModelName(str, Enum):
    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    MULTILINGUAL_E5_LARGE = "multilingual-e5-large"


class ModelFamily(str, Enum):
    OPEN_AI = "openai"
    MINI_LM = "mini_lm"
    E5 = "e5"


class EmbeddingModel(BaseModel):
    name: EmbeddingModelName
    family: ModelFamily
    open_source: bool
    dimensions: Optional[int] = None
    max_input: Optional[int] = None
    selectable: bool = True
    stability: ModelStability = ModelStability.STABLE
    hosting: ModelHostingLocation = ModelHostingLocation.USA
    can_access: bool = True
    hf_link: Optional[HttpUrl] = None


def supported_models():
    return [
        EmbeddingModel(
            name=EmbeddingModelName.TEXT_EMBEDDING_3_SMALL,
            family=ModelFamily.OPEN_AI,
            open_source=False,
            dimensions=512,
            max_input=8191,
        ),
        EmbeddingModel(
            name=EmbeddingModelName.TEXT_EMBEDDING_ADA_002,
            family=ModelFamily.OPEN_AI,
            open_source=False,
            max_input=8191,
        ),
        EmbeddingModel(
            name=EmbeddingModelName.MULTILINGUAL_E5_LARGE,
            family=ModelFamily.E5,
            open_source=True,
            max_input=8191,  # Copied from OpenAI models
            stability=ModelStability.EXPERIMENTAL,
            hosting=ModelHostingLocation.EU,
            hf_link="https://huggingface.co/intfloat/multilingual-e5-large",
        ),
    ]


@lru_cache
def model_string_to_model():
    return {model.name: model for model in supported_models()}


def get_embedding_model(model_name: str) -> EmbeddingModel:
    return model_string_to_model().get(model_name, None)
