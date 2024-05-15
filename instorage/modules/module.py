from enum import Enum

from pydantic import BaseModel, ConfigDict

from instorage.main.models import DateTimeModelMixin, IDModelMixin


class Modules(str, Enum):
    EU_HOSTING = "eu_hosting"


class ModuleBase(BaseModel):
    name: Modules


class ModuleInDB(DateTimeModelMixin, ModuleBase, IDModelMixin):
    model_config = ConfigDict(from_attributes=True)


class ModuleId(BaseModel):
    id: int
