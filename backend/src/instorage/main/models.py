from copy import deepcopy
from datetime import datetime
from enum import Enum
from typing import Any, Generic, Optional, Tuple, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field, create_model
from pydantic.fields import FieldInfo

from instorage.main.exceptions import ErrorCodes

T = TypeVar("T")


class ResourcePermissions(Enum):
    READ = "read"
    CREATE = "create"
    EDIT = "edit"
    DELETE = "delete"
    ADD = "add"
    REMOVE = "remove"


# Taken from https://stackoverflow.com/questions/67699451/make-every-field-as-optional-with-pydantic
def partial_model(model: Type[BaseModel]):
    def make_field_optional(
        field: FieldInfo, default: Any = None
    ) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new

    return create_model(
        f"Partial{model.__name__}",
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        },
    )


class ModelId(BaseModel):
    id: UUID


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class InDB(ModelId, DateTimeModelMixin):
    model_config = ConfigDict(from_attributes=True)


class ResourcePermissionsMixin(BaseModel):
    permissions: list[ResourcePermissions] = []


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T] = Field(description="List of items returned in the response")

    @computed_field(description="Number of items returned in the response")
    @property
    def count(self) -> int:
        return len(self.items)


class PaginatedResponseWithPublicItems(PaginatedResponse):
    public_count: int = Field(description="Number of items returned in the response")
    public_items: list[T] = Field(description="List of items returned in the response")


class PaginatedPermissions(PaginatedResponse, ResourcePermissionsMixin):
    pass


class GeneralError(BaseModel):
    message: str
    intric_error_code: ErrorCodes


class DeleteResponse(BaseModel):
    success: bool


class SuccessResponse(DeleteResponse):
    pass


class IdAndName(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)


class PublicReference(InDB):
    name: str
