from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ValidationInfo, field_validator
from pydantic.networks import HttpUrl

from intric.main.models import InDB
from intric.modules.module import ModuleInDB


class PrivacyPolicyMixin(BaseModel):
    privacy_policy: Optional[HttpUrl] = None


class TenantBase(BaseModel):
    name: str
    display_name: Optional[str] = None
    quota_limit: int = Field(
        default=10 * 1024**3, description="Size in bytes. Default is 10 GB"
    )
    domain: Optional[str] = None
    zitadel_org_id: Optional[str] = None
    provisioning: bool = False

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
    provisioning: bool = False

    modules: list[ModuleInDB] = []


class TenantUpdatePublic(BaseModel):
    display_name: Optional[str] = None
    quota_limit: Optional[int] = None
    domain: Optional[str] = None
    zitadel_org_id: Optional[str] = None
    provisioning: Optional[bool] = None


class TenantUpdate(TenantUpdatePublic):
    id: UUID
