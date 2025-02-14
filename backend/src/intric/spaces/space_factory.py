from typing import TYPE_CHECKING

from intric.ai_models.embedding_models.embedding_model import EmbeddingModel
from intric.completion_models.domain import CompletionModelFactory
from intric.database.tables.ai_models_table import (
    CompletionModels,
    CompletionModelSettings,
    EmbeddingModels,
)
from intric.database.tables.groups_table import Groups
from intric.database.tables.spaces_table import Spaces
from intric.groups.api.group_models import Group
from intric.services.service import Service
from intric.spaces.api.space_models import SpaceMember
from intric.spaces.space import Space
from intric.websites.crawl_dependencies.crawl_models import CrawlRunSparse
from intric.websites.website_models import WebsiteMetadata, WebsiteSparse

if TYPE_CHECKING:
    from uuid import UUID

    from intric.apps import App
    from intric.assistants.assistant import Assistant
    from intric.users.user import UserInDB


class SpaceFactory:

    @staticmethod
    def create_space(
        name: str, description: str = None, user_id: "UUID" = None
    ) -> Space:
        return Space(
            id=None,
            tenant_id=None,
            user_id=user_id,
            name=name,
            description=description,
            embedding_models=[],
            completion_models=[],
            default_assistant=None,
            assistants=[],
            apps=[],
            services=[],
            websites=[],
            groups=[],
            members={},
        )

    @staticmethod
    def create_space_from_db(
        space_in_db: Spaces,
        user: "UserInDB",
        groups_in_db: list[tuple[Groups, int]] = [],
        completion_models_in_db: list[
            tuple[CompletionModels, CompletionModelSettings]
        ] = [],
        embedding_models_in_db: list[tuple[EmbeddingModels, bool]] = [],
        default_assistant: "Assistant" = None,
        assistants: list["Assistant"] = [],
        apps: list["App"] = [],
    ) -> Space:
        completion_models = [
            CompletionModelFactory.create_from_db(
                completion_model=completion_model,
                completion_model_settings=completion_model_settings,
                user=user,
            )
            for completion_model, completion_model_settings in completion_models_in_db
        ]
        embedding_models = [
            EmbeddingModel(**model.to_dict(), is_org_enabled=is_org_enabled)
            for model, is_org_enabled in embedding_models_in_db
        ]
        members = {
            space_user.user_id: SpaceMember(
                **space_user.user.to_dict(), role=space_user.role
            )
            for space_user in space_in_db.members
            if space_user.user.deleted_at is None
        }
        groups = [
            Group(
                **group.to_dict(),
                num_info_blobs=info_blob_count,
                embedding_model=EmbeddingModel.model_validate(group.embedding_model),
            )
            for group, info_blob_count in groups_in_db
        ]
        assistants = [assistant for assistant in assistants if not assistant.is_default]
        services = [Service.model_validate(service) for service in space_in_db.services]
        websites = [
            WebsiteSparse(
                **website.to_dict(),
                metadata=WebsiteMetadata(size=website.size),
                latest_crawl=CrawlRunSparse.model_validate(website.latest_crawl),
                embedding_model=EmbeddingModel.model_validate(website.embedding_model),
            )
            for website in space_in_db.websites
        ]

        # Set the tools of the default assistant
        if default_assistant is not None:
            default_assistant.tool_assistants = assistants

        return Space(
            created_at=space_in_db.created_at,
            updated_at=space_in_db.updated_at,
            id=space_in_db.id,
            tenant_id=space_in_db.tenant_id,
            user_id=space_in_db.user_id,
            name=space_in_db.name,
            description=space_in_db.description,
            embedding_models=embedding_models,
            default_assistant=default_assistant,
            assistants=assistants,
            apps=apps,
            services=services,
            groups=groups,
            websites=websites,
            completion_models=completion_models,
            members=members,
        )
