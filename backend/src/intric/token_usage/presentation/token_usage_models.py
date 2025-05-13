from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import UUID

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from intric.token_usage.domain.token_usage_models import (
        ModelTokenUsage as DomainModelTokenUsage,
    )
    from intric.token_usage.domain.token_usage_models import (
        TokenUsageSummary as DomainTokenUsageSummary,
    )


class ModelUsage(BaseModel):
    model_id: UUID
    model_name: str
    model_nickname: str = Field(..., description="User-friendly name of the model")
    model_org: str | None = Field(default=None, description="Organization providing the model")
    input_token_usage: int = Field(..., description="Number of tokens used for input prompts")
    output_token_usage: int = Field(..., description="Number of tokens used for model outputs")
    total_token_usage: int = Field(..., description="Total tokens (input + output)")
    request_count: int = Field(..., description="Number of requests made with this model")

    @classmethod
    def from_domain(cls, domain_model: "DomainModelTokenUsage") -> "ModelUsage":
        return cls(
            model_id=domain_model.model_id,
            model_name=domain_model.model_name,
            model_nickname=domain_model.model_nickname,
            model_org=domain_model.model_org,
            input_token_usage=domain_model.input_token_usage,
            output_token_usage=domain_model.output_token_usage,
            total_token_usage=domain_model.total_token_usage,
            request_count=domain_model.request_count,
        )


class TokenUsageSummary(BaseModel):
    start_date: datetime
    end_date: datetime
    models: List[ModelUsage]
    total_input_token_usage: int = Field(
        ..., description="Total input token usage across all models"
    )
    total_output_token_usage: int = Field(
        ..., description="Total output token usage across all models"
    )
    total_token_usage: int = Field(
        ..., description="Total combined token usage across all models"
    )

    @classmethod
    def from_domain(cls, domain: "DomainTokenUsageSummary") -> "TokenUsageSummary":
        return cls(
            start_date=domain.start_date,
            end_date=domain.end_date,
            models=[ModelUsage.from_domain(model) for model in domain.models],
            total_input_token_usage=domain.total_input_token_usage,
            total_output_token_usage=domain.total_output_token_usage,
            total_token_usage=domain.total_token_usage,
        )
