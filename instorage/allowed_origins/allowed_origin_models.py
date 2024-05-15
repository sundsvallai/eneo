from pydantic import BaseModel

from instorage.main.models import InDB, Public


class AllowedOrigin(BaseModel):
    url: str


class AllowedOriginInDB(AllowedOrigin, InDB):
    tenant_id: int


class AllowedOriginPublic(AllowedOrigin, Public):
    pass
