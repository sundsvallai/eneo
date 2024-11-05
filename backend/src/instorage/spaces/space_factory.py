# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

from uuid import UUID

from instorage.ai_models.completion_models.completion_model import CompletionModelSparse
from instorage.ai_models.embedding_models.embedding_model import EmbeddingModelSparse
from instorage.assistants.api.assistant_models import AssistantSparse
from instorage.database.tables.groups_table import Groups
from instorage.database.tables.spaces_table import Spaces
from instorage.groups.group import GroupMetadata, GroupSparse
from instorage.main.models import IdAndName
from instorage.services.service import ServiceSparse
from instorage.spaces.api.space_models import SpaceMember
from instorage.spaces.space import Space
from instorage.websites.website_models import WebsiteSparse


class SpaceFactory:
    @staticmethod
    def create_space(name: str, description: str = None, user_id: UUID = None) -> Space:
        return Space(
            id=None,
            tenant_id=None,
            user_id=user_id,
            name=name,
            description=description,
            embedding_models=[],
            completion_models=[],
            assistants=[],
            services=[],
            websites=[],
            groups=[],
            members={},
        )

    @staticmethod
    def create_space_from_db(
        space_in_db: Spaces, groups_in_db: list[tuple[Groups, int]] = []
    ) -> Space:
        embedding_models = [
            EmbeddingModelSparse.model_validate(model)
            for model in space_in_db.embedding_models
        ]
        completion_models = [
            CompletionModelSparse.model_validate(model)
            for model in space_in_db.completion_models
        ]
        members = {
            space_user.user_id: SpaceMember(
                **space_user.user.to_dict(), role=space_user.role
            )
            for space_user in space_in_db.members
        }
        groups = [
            GroupSparse(
                **group.to_dict(),
                metadata=GroupMetadata(num_info_blobs=info_blob_count),
                embedding_model=IdAndName.model_validate(group.embedding_model)
            )
            for group, info_blob_count in groups_in_db
        ]
        assistants = [
            AssistantSparse.model_validate(assistant)
            for assistant in space_in_db.assistants
        ]
        services = [
            ServiceSparse.model_validate(service) for service in space_in_db.services
        ]
        websites = [
            WebsiteSparse.model_validate(website) for website in space_in_db.websites
        ]

        return Space(
            created_at=space_in_db.created_at,
            updated_at=space_in_db.updated_at,
            id=space_in_db.id,
            tenant_id=space_in_db.tenant_id,
            user_id=space_in_db.user_id,
            name=space_in_db.name,
            description=space_in_db.description,
            embedding_models=embedding_models,
            assistants=assistants,
            services=services,
            groups=groups,
            websites=websites,
            completion_models=completion_models,
            members=members,
        )
