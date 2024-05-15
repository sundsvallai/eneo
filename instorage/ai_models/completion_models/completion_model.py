from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from instorage.ai_models.completion_models.llms import (
    ModelFamily,
    ModelHostingLocation,
    ModelStability,
)
from instorage.main.models import InDBOnlyUuid, partial_model


class CompletionModelBase(BaseModel):
    name: str
    nickname: str
    family: ModelFamily
    token_limit: int
    selectable: bool
    nr_billion_parameters: Optional[int] = None
    hf_link: Optional[str] = None
    stability: ModelStability
    hosting: ModelHostingLocation


class CompletionModelCreate(CompletionModelBase):
    pass


@partial_model
class CompletionModelUpdate(CompletionModelBase):
    id: UUID


class CompletionModelInDB(CompletionModelBase, InDBOnlyUuid):
    pass


class CompletionModelPublic(CompletionModelInDB):
    can_access: Optional[bool] = True
