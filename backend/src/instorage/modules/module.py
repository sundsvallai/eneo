from enum import Enum

from pydantic import BaseModel

from instorage.main.models import InDB


class Modules(str, Enum):
    """
    Any change to these enums will result in database changes
    """

    EU_HOSTING = "eu_hosting"
    INTRIC_APPLICATIONS = "intric-applications"


class ModuleBase(BaseModel):
    name: Modules | str


class ModuleInDB(InDB, ModuleBase):
    pass
