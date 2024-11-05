# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

from instorage.assistants.api.assistant_models import AssistantPublic, AssistantSparse
from instorage.assistants.assistant import Assistant
from instorage.groups.group import GroupInDB, GroupMetadata, GroupSparse
from instorage.main.models import PaginatedPermissions, ResourcePermissions
from instorage.services.service import Service, ServiceSparse
from instorage.spaces.api.space_models import (
    Applications,
    CreateSpaceGroupsResponse,
    CreateSpaceServiceResponse,
    CreateSpaceWebsitesResponse,
    Knowledge,
    SpaceMember,
    SpacePublic,
)
from instorage.spaces.space import Space
from instorage.users.user import UserInDB
from instorage.websites.website_models import Website, WebsiteSparse


class SpaceAssembler:
    def __init__(self, user: UserInDB):
        self.user = user

    def _set_permissions_on_resource(
        self,
        space: Space,
        resource: AssistantSparse | WebsiteSparse | GroupSparse | ServiceSparse,
    ):
        resource_permissions = []
        if space.can_read_resource(self.user):
            resource_permissions.append(ResourcePermissions.READ)

        if space.can_edit_resource(self.user):
            resource_permissions.append(ResourcePermissions.EDIT)

        if space.can_delete_resource(self.user, resource.user_id):
            resource_permissions.append(ResourcePermissions.DELETE)

        resource.permissions = resource_permissions

    def _set_permissions_on_resources(self, space: Space):
        for assistant in space.assistants:
            self._set_permissions_on_resource(space, assistant)

        for service in space.services:
            self._set_permissions_on_resource(space, service)

        for group in space.groups:
            self._set_permissions_on_resource(space, group)

        for website in space.websites:
            self._set_permissions_on_resource(space, website)

    def _get_assistant_permissions(self, space: Space):
        if space.can_create_assistants(self.user):
            return [ResourcePermissions.READ, ResourcePermissions.CREATE]

        return []

    def _get_service_permissions(self, space: Space):
        if space.can_create_services(self.user):
            return [ResourcePermissions.READ, ResourcePermissions.CREATE]

        return []

    def _get_group_permissions(self, space: Space):
        if space.can_create_groups(self.user):
            return [ResourcePermissions.READ, ResourcePermissions.CREATE]

        return []

    def _get_website_permissions(self, space: Space):
        if space.can_create_websites(self.user):
            return [ResourcePermissions.READ, ResourcePermissions.CREATE]

        return []

    def _get_member_permissions(self, space: Space):
        permissions = []
        if space.can_read_members(self.user):
            permissions.append(ResourcePermissions.READ)

        if space.can_edit(self.user):
            permissions.extend(
                [
                    ResourcePermissions.ADD,
                    ResourcePermissions.EDIT,
                    ResourcePermissions.REMOVE,
                ]
            )

        return permissions

    def _get_space_permissions(self, space: Space):
        permissions = []
        if space.can_read(self.user):
            permissions.append(ResourcePermissions.READ)

        if space.can_edit(self.user):
            permissions.extend([ResourcePermissions.EDIT, ResourcePermissions.DELETE])

        return permissions

    def _sort_members(self, space: Space):
        if not space.members:
            return []

        return [space.members[self.user.id]] + [
            member for member in space.members.values() if member.id != self.user.id
        ]

    def from_space_to_model(self, space: Space):
        self._set_permissions_on_resources(space)
        applications = Applications(
            assistants=PaginatedPermissions[AssistantSparse](
                items=space.assistants,
                permissions=self._get_assistant_permissions(space),
            ),
            services=PaginatedPermissions[ServiceSparse](
                items=space.services,
                permissions=self._get_service_permissions(space),
            ),
        )
        knowledge = Knowledge(
            groups=PaginatedPermissions[GroupSparse](
                items=space.groups,
                permissions=self._get_group_permissions(space),
            ),
            websites=PaginatedPermissions[WebsiteSparse](
                items=space.websites,
                permissions=self._get_website_permissions(space),
            ),
        )
        members = PaginatedPermissions[SpaceMember](
            items=self._sort_members(space),
            permissions=self._get_member_permissions(space),
        )
        personal = space.user_id is not None
        return SpacePublic(
            created_at=space.created_at,
            updated_at=space.updated_at,
            id=space.id,
            name=space.name,
            description=space.description,
            embedding_models=space.embedding_models,
            completion_models=space.completion_models,
            applications=applications,
            knowledge=knowledge,
            members=members,
            personal=personal,
            permissions=self._get_space_permissions(space),
        )

    @staticmethod
    def from_assistant_to_model(assistant: Assistant):
        return AssistantPublic(
            id=assistant.id,
            name=assistant.name,
            prompt=assistant.prompt,
            completion_model_kwargs=assistant.completion_model_kwargs,
            logging_enabled=assistant.logging_enabled,
            groups=assistant.groups,
            websites=assistant.websites,
            completion_model=assistant.completion_model,
            user=assistant.user,
            created_at=assistant.created_at,
            updated_at=assistant.updated_at,
        )

    @staticmethod
    def from_service_to_model(service: Service):
        return CreateSpaceServiceResponse(**service.model_dump())

    @staticmethod
    def from_group_to_model(group: GroupInDB, count: int = 0):
        return CreateSpaceGroupsResponse(
            **group.model_dump(),
            metadata=GroupMetadata(num_info_blobs=count),
        )

    @staticmethod
    def from_website_to_model(website: Website):
        return CreateSpaceWebsitesResponse(**website.model_dump())
