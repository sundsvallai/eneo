from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, computed_field

T = TypeVar("T", bound=BaseModel)


class BaseListModel(BaseModel, Generic[T]):
    items: list[T]

    @computed_field
    def count(self) -> int:
        return len(self.items)


class Integration(BaseModel):
    id: UUID
    name: str
    description: str


class IntegrationList(BaseListModel[Integration]):
    pass


class TenantIntegration(Integration):
    enabled: bool


class TenantIntegrationList(BaseListModel[TenantIntegration]):
    pass


class UserIntegration(Integration):
    connected: bool


class UserIntegrationList(BaseListModel[UserIntegration]):
    pass
