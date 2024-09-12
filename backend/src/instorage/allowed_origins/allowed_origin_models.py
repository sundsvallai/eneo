from uuid import UUID

from pydantic import BaseModel

from instorage.main.models import InDB


class AllowedOrigin(BaseModel):
    url: str


class AllowedOriginCreate(AllowedOrigin):
    tenant_id: UUID


class AllowedOriginInDB(AllowedOriginCreate, InDB):
    pass


class AllowedOriginPublic(AllowedOrigin, InDB):
    pass
