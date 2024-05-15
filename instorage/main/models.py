from copy import deepcopy
from datetime import datetime
from typing import Any, Generic, Optional, Tuple, Type, TypeVar
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, create_model
from pydantic.fields import FieldInfo

T = TypeVar("T")


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


class IDModelMixin(BaseModel):
    id: int


class ModelUUID(BaseModel):
    id: UUID


class IdWithUuidMixin(BaseModel):
    id: int
    uuid: UUID


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class InDB(IdWithUuidMixin, DateTimeModelMixin):
    model_config = ConfigDict(from_attributes=True)


# TODO: change name when integer ids are removed
class InDBOnlyUuid(ModelUUID, DateTimeModelMixin):
    model_config = ConfigDict(from_attributes=True)


class Public(DateTimeModelMixin):
    id: UUID = Field(validation_alias=AliasChoices("uuid", "id"))


class PaginatedResponse(BaseModel, Generic[T]):
    count: int = Field(description="Number of items returned in the response")
    items: list[T] = Field(description="List of items returned in the response")


class PaginatedResponseWithPublicItems(PaginatedResponse):
    public_count: int = Field(description="Number of items returned in the response")
    public_items: list[T] = Field(description="List of items returned in the response")


class GeneralError(BaseModel):
    message: str


class DeleteResponse(BaseModel):
    success: bool
