# MIT license

from datetime import datetime
from enum import Enum
from uuid import UUID

from instorage.ai_models.completion_models.completion_model import (
    CompletionModelPublic,
    CompletionModelSparse,
)
from instorage.ai_models.embedding_models.embedding_model import (
    EmbeddingModelPublic,
    EmbeddingModelSparse,
)
from instorage.assistants.api.assistant_models import AssistantSparse
from instorage.groups.group import GroupSparse
from instorage.main.config import SETTINGS
from instorage.main.exceptions import BadRequestException, UnauthorizedException
from instorage.modules.module import Modules
from instorage.roles.permissions import Permission
from instorage.services.service import ServiceSparse
from instorage.spaces.api.space_models import SpaceMember, SpaceRole
from instorage.users.user import UserInDB
from instorage.websites.website_models import WebsiteSparse

UNAUTHORIZED_EXCEPTION_MESSAGE = "Unauthorized. User has no permissions to access."


class SpacePermissionsActions(Enum):
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class Space:
    def __init__(
        self,
        id: UUID | None,
        tenant_id: UUID | None,
        user_id: UUID | None,
        name: str,
        description: str | None,
        embedding_models: list[EmbeddingModelSparse],
        completion_models: list[CompletionModelSparse],
        assistants: list[AssistantSparse],
        services: list[ServiceSparse],
        websites: list[WebsiteSparse],
        groups: list[GroupSparse],
        members: dict[UUID, SpaceMember],
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        self.id = id
        self.tenant_id = tenant_id
        self.user_id = user_id
        self.name = name
        self.description = description
        self._embedding_models = embedding_models
        self._completion_models = completion_models
        self.assistants = assistants
        self.services = services
        self.websites = websites
        self.groups = groups
        self.members = members
        self.created_at = created_at
        self.updated_at = updated_at

    def _get_admin_ids(self):
        return [
            user_id
            for user_id, user in self.members.items()
            if user.role == SpaceRole.ADMIN
        ]

    def _get_editor_ids(self):
        return [
            user_id
            for user_id, user in self.members.items()
            if user.role == SpaceRole.EDITOR
        ]

    def _get_member_ids(self):
        return self.members.keys()

    def is_personal(self):
        return self.user_id is not None

    def can_read(self, user: UserInDB):
        if self.is_personal():
            return user.id == self.user_id

        return user.id in self._get_member_ids()

    def can_edit(self, user: UserInDB):
        if self.is_personal():
            # No one can edit the personal space
            return False

        return user.id in self._get_admin_ids()

    def can_create_assistants(self, user: UserInDB):
        if self.is_personal():
            return Permission.ASSISTANTS in user.permissions

        return user.id in self._get_member_ids()

    def can_create_services(self, user: UserInDB):
        if Modules.INTRIC_APPLICATIONS not in user.modules:
            return False

        if self.is_personal():
            return Permission.SERVICES in user.permissions

        return user.id in self._get_member_ids()

    def can_create_groups(self, user: UserInDB):
        if self.is_personal():
            return Permission.COLLECTIONS in user.permissions

        return user.id in self._get_member_ids()

    def can_create_websites(self, user: UserInDB):
        if not SETTINGS.using_intric_proprietary:
            # Websites is a proprietary feature
            return False

        if self.is_personal():
            return Permission.WEBSITES in user.permissions

        return user.id in self._get_member_ids()

    def can_read_resource(self, user: UserInDB):
        if self.is_personal():
            return user.id == self.user_id

        return user.id in self._get_member_ids()

    def can_edit_resource(self, user: UserInDB):
        if self.is_personal():
            return user.id == self.user_id

        return user.id in self._get_member_ids()

    def can_delete_resource(self, user: UserInDB, owner_id: UUID):
        if self.is_personal():
            return user.id == self.user_id

        return user.id == owner_id or user.id in self._get_admin_ids()

    def can_read_members(self, user: UserInDB):
        if self.is_personal():
            # No one can read the members of a personal space
            return False

        return user.id in self._get_member_ids()

    def is_embedding_model_in_space(self, embedding_model_id: UUID | None) -> bool:
        return self.is_personal() or embedding_model_id in [
            model.id for model in self.embedding_models
        ]

    def is_completion_model_in_space(self, completion_model_id: UUID | None) -> bool:
        return self.is_personal() or completion_model_id in [
            model.id for model in self.completion_models
        ]

    def is_group_in_space(self, group_id: UUID) -> bool:
        return group_id in [group.id for group in self.groups]

    def is_website_in_space(self, website_id: UUID) -> bool:
        return website_id in [website.id for website in self.websites]

    def get_member(self, member_id: UUID) -> SpaceMember:
        return self.members[member_id]

    def get_latest_embedding_model(self) -> EmbeddingModelSparse:
        if not self.embedding_models:
            return

        sorted_embedding_models = sorted(
            self.embedding_models, key=lambda model: model.created_at, reverse=True
        )

        return sorted_embedding_models[0]

    def get_latest_completion_model(self) -> CompletionModelSparse:
        if not self.completion_models:
            return

        sorted_completion_models = sorted(
            self.completion_models, key=lambda model: model.created_at, reverse=True
        )

        return sorted_completion_models[0]

    @property
    def embedding_models(self):
        return self._embedding_models

    @embedding_models.setter
    def embedding_models(self, embedding_models: list[EmbeddingModelPublic]):
        for model in embedding_models:
            if not model.can_access:
                raise UnauthorizedException(UNAUTHORIZED_EXCEPTION_MESSAGE)

        self._embedding_models = embedding_models

    @property
    def completion_models(self):
        return self._completion_models

    @completion_models.setter
    def completion_models(self, completion_models: list[CompletionModelPublic]):
        for model in completion_models:
            if not model.can_access:
                raise UnauthorizedException(UNAUTHORIZED_EXCEPTION_MESSAGE)

        self._completion_models = completion_models

    def update(
        self,
        name: str = None,
        description: str = None,
        embedding_models: list[EmbeddingModelPublic] = None,
        completion_models: list[CompletionModelPublic] = None,
    ):
        if name is not None:
            if self.is_personal():
                raise BadRequestException("Can not change name of personal space")

            self.name = name

        if description is not None:
            if self.is_personal():
                raise BadRequestException(
                    "Can not change description of personal space"
                )

            self.description = description

        if completion_models is not None:
            if self.is_personal():
                raise BadRequestException(
                    "Can not add completion models to personal space"
                )

            self.completion_models = completion_models

        if embedding_models is not None:
            if self.is_personal():
                raise BadRequestException(
                    "Can not add embedding models to personal space"
                )

            self.embedding_models = embedding_models

    def add_member(self, user: SpaceMember):
        if self.is_personal():
            raise BadRequestException("Can not add members to personal space")

        if user.id in self._get_member_ids():
            raise BadRequestException("User is already a member of the space")

        self.members[user.id] = user

    def remove_member(self, user_id: UUID):
        if user_id not in self._get_member_ids():
            raise BadRequestException("User is not a member of the space")

        del self.members[user_id]

    def change_member_role(self, user_id: UUID, new_role: SpaceRole):
        if user_id not in self._get_member_ids():
            raise BadRequestException("User is not a member of the space")

        self.members[user_id].role = new_role
