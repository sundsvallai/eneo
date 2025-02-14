from typing import TYPE_CHECKING

from intric.ai_models.embedding_models.embedding_model import EmbeddingModelSparse
from intric.assistants.api.assistant_models import AssistantSparse
from intric.groups.api.group_models import Group, GroupMetadata, GroupPublicWithMetadata
from intric.groups.api.group_protocol import to_group_public_with_metadata
from intric.main.models import PaginatedPermissions, ResourcePermission
from intric.services.service import Service, ServiceSparse
from intric.spaces.api.space_models import (
    Applications,
    AppSparse,
    CreateSpaceGroupsResponse,
    CreateSpaceServiceResponse,
    Knowledge,
    SpaceDashboard,
    SpaceMember,
    SpacePublic,
    SpaceRole,
    SpaceSparse,
)
from intric.spaces.space import Space
from intric.users.user import UserInDB
from intric.websites.website_models import WebsiteSparse

if TYPE_CHECKING:
    from intric.actors import ActorManager
    from intric.assistants.api.assistant_assembler import AssistantAssembler
    from intric.assistants.assistant import Assistant
    from intric.completion_models.presentation import CompletionModelAssembler


class SpaceAssembler:
    def __init__(
        self,
        user: UserInDB,
        assistant_assembler: "AssistantAssembler",
        completion_model_assembler: "CompletionModelAssembler",
        actor_manager: "ActorManager",
    ):
        self.user = user
        self.assistant_assembler = assistant_assembler
        self.completion_model_assembler = completion_model_assembler
        self.actor_manager = actor_manager

    def _set_permissions_on_resources(self, space: Space):
        actor = self.actor_manager.get_space_actor_from_space(space=space)

        for assistant in space.assistants:
            assistant.permissions = actor.get_assistant_permissions(assistant=assistant)

        for app in space.apps:
            app.permissions = actor.get_app_permissions()

        for service in space.services:
            service.permissions = actor.get_service_permissions()

        for group in space.groups:
            group.permissions = actor.get_group_permissions()

        for website in space.websites:
            website.permissions = actor.get_website_permissions()

    def _get_assistant_permissions(self, space: Space):
        actor = self.actor_manager.get_space_actor_from_space(space=space)
        permissions = []

        if actor.can_read_assistants():
            permissions.append(ResourcePermission.READ)
        if actor.can_create_assistants():
            permissions.append(ResourcePermission.CREATE)
        if actor.can_publish_assistants():
            permissions.append(ResourcePermission.PUBLISH)

        return permissions

    def _get_app_permissions(self, space: Space):
        actor = self.actor_manager.get_space_actor_from_space(space=space)
        permissions = []

        if actor.can_read_apps():
            permissions.append(ResourcePermission.READ)
        if actor.can_create_apps():
            permissions.append(ResourcePermission.CREATE)
        if actor.can_publish_apps():
            permissions.append(ResourcePermission.PUBLISH)

        return permissions

    def _get_service_permissions(self, space: Space):
        actor = self.actor_manager.get_space_actor_from_space(space=space)
        permissions = []

        if actor.can_read_services():
            permissions.append(ResourcePermission.READ)
        if actor.can_create_services():
            permissions.append(ResourcePermission.CREATE)

        return permissions

    def _get_group_permissions(self, space: Space):
        actor = self.actor_manager.get_space_actor_from_space(space=space)
        permissions = []

        if actor.can_read_groups():
            permissions.append(ResourcePermission.READ)
        if actor.can_create_groups():
            permissions.append(ResourcePermission.CREATE)

        return permissions

    def _get_website_permissions(self, space: Space):
        actor = self.actor_manager.get_space_actor_from_space(space=space)
        permissions = []

        if actor.can_read_websites():
            permissions.append(ResourcePermission.READ)
        if actor.can_create_websites():
            permissions.append(ResourcePermission.CREATE)

        return permissions

    def _get_default_assistant_permissions(self, space: Space):
        actor = self.actor_manager.get_space_actor_from_space(space=space)
        permissions = []

        if actor.can_read_default_assistant():
            permissions.append(ResourcePermission.READ)

        if actor.can_edit_default_assistant():
            permissions.append(ResourcePermission.EDIT)

        return permissions

    def _get_member_permissions(self, space: Space):
        actor = self.actor_manager.get_space_actor_from_space(space=space)
        permissions = []

        if actor.can_read_members():
            permissions.append(ResourcePermission.READ)

        if actor.can_edit_space():
            permissions.extend(
                [
                    ResourcePermission.ADD,
                    ResourcePermission.EDIT,
                    ResourcePermission.REMOVE,
                ]
            )

        return permissions

    def _get_space_permissions(self, space: Space):
        actor = self.actor_manager.get_space_actor_from_space(space=space)
        permissions = []

        if actor.can_read_space():
            permissions.append(ResourcePermission.READ)

        if actor.can_edit_space():
            permissions.append(ResourcePermission.EDIT)

        if actor.can_delete_space():
            permissions.append(ResourcePermission.DELETE)

        return permissions

    def _sort_members(self, space: Space):
        if not space.members:
            return []

        return [space.members[self.user.id]] + [
            member for member in space.members.values() if member.id != self.user.id
        ]

    def _get_assistant_model(self, assistant: "Assistant"):
        return AssistantSparse(
            created_at=assistant.created_at,
            updated_at=assistant.updated_at,
            id=assistant.id,
            name=assistant.name,
            completion_model_kwargs=assistant.completion_model_kwargs,
            logging_enabled=assistant.logging_enabled,
            user_id=assistant.user.id,
            published=assistant.published,
            permissions=assistant.permissions,
        )

    def _get_applications_model(self, space: Space) -> Applications:
        actor = self.actor_manager.get_space_actor_from_space(space=space)
        return Applications(
            assistants=PaginatedPermissions[AssistantSparse](
                items=[
                    self._get_assistant_model(assistant)
                    for assistant in space.assistants
                    if actor.can_read_assistant(assistant=assistant)
                ],
                permissions=self._get_assistant_permissions(space),
            ),
            apps=PaginatedPermissions[AppSparse](
                items=[app for app in space.apps if actor.can_read_app(app=app)],
                permissions=self._get_app_permissions(space),
            ),
            services=PaginatedPermissions[ServiceSparse](
                items=[
                    service for service in space.services if actor.can_read_services()
                ],
                permissions=self._get_service_permissions(space),
            ),
        )

    def _get_knowledge_model(self, space: Space) -> Knowledge:
        actor = self.actor_manager.get_space_actor_from_space(space=space)
        return Knowledge(
            groups=PaginatedPermissions[GroupPublicWithMetadata](
                items=(
                    [
                        to_group_public_with_metadata(
                            group=group, num_info_blobs=group.num_info_blobs
                        )
                        for group in space.groups
                    ]
                    if actor.can_read_groups()
                    else []
                ),
                permissions=self._get_group_permissions(space),
            ),
            websites=PaginatedPermissions[WebsiteSparse](
                items=space.websites if actor.can_read_websites() else [],
                permissions=self._get_website_permissions(space),
            ),
        )

    def from_space_to_model(self, space: Space) -> SpacePublic:
        actor = self.actor_manager.get_space_actor_from_space(space=space)
        self._set_permissions_on_resources(space)
        applications = self._get_applications_model(space)
        knowledge = self._get_knowledge_model(space)
        members = PaginatedPermissions[SpaceMember](
            items=self._sort_members(space),
            permissions=self._get_member_permissions(space),
        )
        embedding_models = [
            EmbeddingModelSparse(**model.model_dump())
            for model in space.embedding_models
            if model.is_org_enabled
        ]
        completion_models = [
            self.completion_model_assembler.from_completion_model_to_model(
                completion_model=model
            )
            for model in space.completion_models
            if model.is_org_enabled
        ]
        default_assistant = (
            self.assistant_assembler.from_assistant_to_default_assistant_model(
                space.default_assistant,
                permissions=self._get_default_assistant_permissions(space),
            )
        )
        available_roles = [
            SpaceRole(value=role) for role in actor.get_available_roles()
        ]

        return SpacePublic(
            created_at=space.created_at,
            updated_at=space.updated_at,
            id=space.id,
            name=space.name,
            description=space.description,
            embedding_models=embedding_models,
            completion_models=completion_models,
            default_assistant=default_assistant,
            applications=applications,
            knowledge=knowledge,
            members=members,
            personal=space.is_personal(),
            permissions=self._get_space_permissions(space),
            available_roles=available_roles,
        )

    def from_space_to_sparse_model(self, space: Space) -> SpaceSparse:
        return SpaceSparse(
            created_at=space.created_at,
            updated_at=space.updated_at,
            id=space.id,
            name=space.name,
            description=space.description,
            personal=space.is_personal(),
            permissions=self._get_space_permissions(space),
        )

    def from_space_to_dashboard_model(self, space: Space) -> SpaceDashboard:
        self._set_permissions_on_resources(space)
        applications = self._get_applications_model(space)

        return SpaceDashboard(
            created_at=space.created_at,
            updated_at=space.updated_at,
            id=space.id,
            name=space.name,
            description=space.description,
            personal=space.is_personal(),
            permissions=self._get_space_permissions(space),
            applications=applications,
        )

    @staticmethod
    def from_service_to_model(
        service: Service, permissions: list[ResourcePermission] = None
    ):
        permissions = permissions or []

        # TODO: Look into how we surface permissions to the presentation layer
        return CreateSpaceServiceResponse(
            **service.model_dump(exclude={"permissions"}), permissions=permissions
        )

    @staticmethod
    def from_group_to_model(group: Group, count: int = 0):
        return CreateSpaceGroupsResponse(
            **group.model_dump(),
            metadata=GroupMetadata(num_info_blobs=count, size=group.size),
        )
