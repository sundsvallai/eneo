from enum import Enum
from typing import Optional

from pydantic import AliasChoices, BaseModel, Field

from instorage.assistants.assistant import AssistantInDB, AssistantInDBWithUser
from instorage.main.models import InDB
from instorage.services.service import ServiceInDB, ServiceInDBWithUser


class FilterType(str, Enum):
    BOOLEAN = "boolean_filter"


class Filter(BaseModel):
    type: FilterType
    chain_breaker_message: str


class FilterInDB(InDB, Filter):
    pass


class Step(BaseModel):
    filter: Optional[Filter] = None
    agent_id: int = Field(validation_alias=AliasChoices("agent_id", "assistant_id"))


class StepInDB(InDB, Step):
    service: ServiceInDB
    filter: Optional[FilterInDB] = None


class WorkflowBase(BaseModel):
    name: str
    steps: list[Step]


class WorkflowInDB(InDB, WorkflowBase):
    steps: list[StepInDB]


# Rebuild models

AssistantInDB.model_rebuild()
AssistantInDBWithUser.model_rebuild()
ServiceInDBWithUser.model_rebuild()
ServiceInDB.model_rebuild()
