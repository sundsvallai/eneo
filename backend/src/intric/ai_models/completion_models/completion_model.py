from enum import Enum
from typing import Any, Optional, Union
from uuid import UUID

from pydantic import BaseModel

from intric.files.file_models import File
from intric.logging.logging import LoggingDetails
from intric.main.models import InDB, partial_model


class CompletionModelFamily(str, Enum):
    OPEN_AI = "openai"
    MISTRAL = "mistral"
    VLLM = "vllm"
    CLAUDE = "claude"
    AZURE = "azure"


class ModelStability(str, Enum):
    STABLE = "stable"
    EXPERIMENTAL = "experimental"


class ModelHostingLocation(str, Enum):
    USA = "usa"
    EU = "eu"
    SWE = "swe"


class Orgs(str, Enum):
    OPENAI = "OpenAI"
    META = "Meta"
    MICROSOFT = "Microsoft"
    ANTHROPIC = "Anthropic"


class CompletionModelBase(BaseModel):
    name: str
    nickname: str
    family: CompletionModelFamily
    token_limit: int
    is_deprecated: bool
    nr_billion_parameters: Optional[int] = None
    hf_link: Optional[str] = None
    stability: ModelStability
    hosting: ModelHostingLocation
    open_source: Optional[bool] = None
    description: Optional[str] = None
    deployment_name: Optional[str] = None
    org: Optional[Orgs] = None
    vision: bool


class CompletionModelCreate(CompletionModelBase):
    pass


@partial_model
class CompletionModelUpdate(CompletionModelBase):
    id: UUID


class CompletionModelUpdateFlags(BaseModel):
    is_org_enabled: Optional[bool] = None
    is_org_default: Optional[bool] = None


class CompletionModel(CompletionModelBase, InDB):
    is_org_enabled: bool = False
    is_org_default: bool = False


class CompletionModelPublic(CompletionModel):
    can_access: bool = False
    is_locked: bool = True


class CompletionModelResponse(BaseModel):
    completion: Union[str, Any]  # Pydantic doesn't support AsyncIterable
    model: CompletionModel
    extended_logging: Optional[LoggingDetails] = None
    total_token_count: int


class Message(BaseModel):
    question: str
    answer: str
    images: list[File] = []


class Context(BaseModel):
    input: str
    token_count: int = 0
    prompt: str = ""
    messages: list[Message] = []
    images: list[File] = []


class ModelKwargs(BaseModel):
    temperature: Optional[float] = None
    top_p: Optional[float] = None


class CompletionModelSparse(CompletionModelBase, InDB):
    pass
