from pydantic import BaseModel, ConfigDict

from instorage.main.models import DateTimeModelMixin, IDModelMixin


class BetaKeyBase(BaseModel):
    key: str


class BetaKeyInDB(BetaKeyBase, IDModelMixin, DateTimeModelMixin):
    used: bool

    model_config = ConfigDict(from_attributes=True)


class BetaKeyPublic(BetaKeyBase):
    used: bool


class BetaKeyCreateResponse(BaseModel):
    keys: list[str]


class BetaKeyCreateRequest(BaseModel):
    number_of_keys: int
