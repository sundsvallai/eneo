from typing import TYPE_CHECKING

from intric.completion_models.domain import (
    CompletionModel,
    ModelFamily,
    ModelHostingLocation,
    ModelOrg,
    ModelStability,
)

if TYPE_CHECKING:
    from intric.database.tables.ai_models_table import (
        CompletionModels,
        CompletionModelSettings,
    )
    from intric.users.user import UserInDB


class CompletionModelFactory:

    @staticmethod
    def create_from_db(
        completion_model: "CompletionModels",
        completion_model_settings: "CompletionModelSettings",
        user: "UserInDB",
    ):
        if completion_model_settings is None:
            is_org_enabled = False
            is_org_default = False
            updated_at = completion_model.updated_at
        else:
            is_org_enabled = completion_model_settings.is_org_enabled
            is_org_default = completion_model_settings.is_org_default
            updated_at = completion_model_settings.updated_at

        org = None if completion_model.org is None else ModelOrg(completion_model.org)

        return CompletionModel(
            user=user,
            id=completion_model.id,
            created_at=completion_model.created_at,
            updated_at=updated_at,
            name=completion_model.nickname,
            model_name=completion_model.name,
            token_limit=completion_model.token_limit,
            vision=completion_model.vision,
            family=ModelFamily(completion_model.family),
            hosting=ModelHostingLocation(completion_model.hosting),
            org=org,
            stability=ModelStability(completion_model.stability),
            open_source=completion_model.open_source,
            description=completion_model.description,
            nr_billion_parameters=completion_model.nr_billion_parameters,
            hf_link=completion_model.hf_link,
            is_deprecated=completion_model.is_deprecated,
            deployment_name=completion_model.deployment_name,
            is_org_enabled=is_org_enabled,
            is_org_default=is_org_default,
        )
