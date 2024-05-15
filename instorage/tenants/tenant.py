from typing import Optional

from pydantic import BaseModel, Field, ValidationInfo, computed_field, field_validator
from pydantic.networks import HttpUrl

from instorage.ai_models.embedding_models.embedding_models import EmbeddingModelName
from instorage.main.models import InDB
from instorage.modules.module import ModuleInDB


class PrivacyPolicyMixin(BaseModel):
    privacy_policy: Optional[HttpUrl] = None


class TenantBase(BaseModel):
    name: str
    display_name: Optional[str] = None
    default_embedding_model: EmbeddingModelName = (
        EmbeddingModelName.TEXT_EMBEDDING_3_SMALL
    )
    quota_limit: int = Field(
        default=1024**3, description="Size in bytes. Default is 1 GB"
    )

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, v: Optional[str], info: ValidationInfo) -> str:
        if v is not None:
            return v

        return info.data["name"]

    @computed_field
    @property
    def alphanumeric(self) -> str:
        return "".join(ch for ch in self.name if ch.isalnum())


class TenantPublic(PrivacyPolicyMixin, TenantBase):
    pass


class TenantInDB(PrivacyPolicyMixin, InDB):
    name: str
    display_name: Optional[str] = None
    default_embedding_model: EmbeddingModelName
    alphanumeric: str
    quota_limit: int

    modules: list[ModuleInDB] = []


class TenantUpdatePublic(BaseModel):
    display_name: Optional[str] = None
    default_embedding_model: Optional[EmbeddingModelName] = None
    quota_limit: Optional[int] = None


class TenantUpdate(TenantUpdatePublic):
    id: int
