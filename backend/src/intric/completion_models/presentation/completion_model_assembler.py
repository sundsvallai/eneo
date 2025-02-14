from typing import TYPE_CHECKING

from intric.completion_models.presentation.completion_model_models import (
    CompletionModelPublic,
)
from intric.server import protocol

if TYPE_CHECKING:
    from intric.completion_models.domain import CompletionModel


class CompletionModelAssembler:

    def from_completion_model_to_model(self, completion_model: "CompletionModel"):
        return CompletionModelPublic(
            id=completion_model.id,
            created_at=completion_model.created_at,
            updated_at=completion_model.updated_at,
            name=completion_model.model_name,
            nickname=completion_model.name,
            token_limit=completion_model.token_limit,
            vision=completion_model.vision,
            family=completion_model.family,
            hosting=completion_model.hosting,
            org=completion_model.org,
            stability=completion_model.stability,
            open_source=completion_model.open_source,
            description=completion_model.description,
            nr_billion_parameters=completion_model.nr_billion_parameters,
            hf_link=completion_model.hf_link,
            is_deprecated=completion_model.is_deprecated,
            deployment_name=completion_model.deployment_name,
            is_org_enabled=completion_model.is_org_enabled,
            is_org_default=completion_model.is_org_default,
            can_access=completion_model.can_access,
            is_locked=completion_model.is_locked,
        )

    def from_completion_models_to_models(
        self, completion_models: list["CompletionModel"]
    ):
        completion_models_public = [
            self.from_completion_model_to_model(completion_model=completion_model)
            for completion_model in completion_models
        ]

        return protocol.to_paginated_response(completion_models_public)
