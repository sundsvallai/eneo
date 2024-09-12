from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ValidationInfo, field_validator
from pydantic.networks import HttpUrl

from instorage.main.models import InDB
from instorage.modules.module import ModuleInDB


class PrivacyPolicyMixin(BaseModel):
    privacy_policy: Optional[HttpUrl] = None


class TenantBase(BaseModel):
    name: str
    display_name: Optional[str] = None
    quota_limit: int = Field(
        default=1024**3, description="Size in bytes. Default is 1 GB"
    )
    domain: Optional[str] = None
    zitadel_org_id: Optional[str] = None

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, v: Optional[str], info: ValidationInfo) -> str:
        if v is not None:
            return v

        return info.data["name"]


class TenantPublic(PrivacyPolicyMixin, TenantBase):
    pass


class TenantInDB(PrivacyPolicyMixin, InDB):
    name: str
    display_name: Optional[str] = None
    quota_limit: int
    domain: Optional[str] = None
    zitadel_org_id: Optional[str] = None

    modules: list[ModuleInDB] = []


class TenantUpdatePublic(BaseModel):
    display_name: Optional[str] = None
    quota_limit: Optional[int] = None
    domain: Optional[str] = None
    zitadel_org_id: Optional[str] = None


class TenantUpdate(TenantUpdatePublic):
    id: UUID
