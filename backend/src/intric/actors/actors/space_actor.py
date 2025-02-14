from enum import Enum
from typing import TYPE_CHECKING, Union

from intric.main.config import SETTINGS
from intric.main.models import ResourcePermission
from intric.modules.module import Modules
from intric.roles.permissions import Permission

if TYPE_CHECKING:
    from intric.apps.apps.app import App
    from intric.assistants.assistant import Assistant
    from intric.spaces.space import Space
    from intric.users.user import UserInDB


class SpaceAction(str, Enum):
    READ = "read"
    CREATE = "create"
    EDIT = "edit"
    DELETE = "delete"
    PUBLISH = "publish"


class SpaceResourceType(str, Enum):
    ASSISTANT = "assistant"
    APP = "app"
    SERVICE = "service"
    GROUP = "group"
    WEBSITE = "website"
    INFO_BLOB = "info blob"
    SPACE = "space"
    MEMBER = "member"
    DEFAULT_ASSISTANT = "default assistant"


class SpaceRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


SHARED_SPACE_PERMISSIONS = {
    SpaceRole.VIEWER: {
        SpaceResourceType.ASSISTANT: {SpaceAction.READ},
        SpaceResourceType.APP: {SpaceAction.READ},
        # Only published resources are readable -- enforced in code
        SpaceResourceType.INFO_BLOB: {SpaceAction.READ},
        SpaceResourceType.SPACE: {
            SpaceAction.READ,
        },
        SpaceResourceType.DEFAULT_ASSISTANT: {
            SpaceAction.READ,
        },
    },
    SpaceRole.EDITOR: {
        SpaceResourceType.ASSISTANT: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            SpaceAction.PUBLISH,
        },
        SpaceResourceType.APP: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            SpaceAction.PUBLISH,
        },
        SpaceResourceType.SERVICE: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            SpaceAction.PUBLISH,
        },
        SpaceResourceType.GROUP: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            # Note: No publish
        },
        SpaceResourceType.WEBSITE: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            # Note: No publish
        },
        SpaceResourceType.INFO_BLOB: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.DELETE,
        },
        SpaceResourceType.SPACE: {
            SpaceAction.READ,
        },
        SpaceResourceType.DEFAULT_ASSISTANT: {
            SpaceAction.READ,
        },
    },
    SpaceRole.ADMIN: {
        SpaceResourceType.ASSISTANT: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            SpaceAction.PUBLISH,
        },
        SpaceResourceType.APP: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            SpaceAction.PUBLISH,
        },
        SpaceResourceType.SERVICE: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            SpaceAction.PUBLISH,
        },
        SpaceResourceType.GROUP: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            # Note: No publish
        },
        SpaceResourceType.WEBSITE: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            # Note: No publish
        },
        SpaceResourceType.INFO_BLOB: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.DELETE,
        },
        SpaceResourceType.SPACE: {
            SpaceAction.READ,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
        },
        SpaceResourceType.MEMBER: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
        },
        SpaceResourceType.DEFAULT_ASSISTANT: {
            SpaceAction.READ,
            SpaceAction.EDIT,
        },
    },
}

PERSONAL_SPACE_PERMISSIONS = {
    SpaceRole.OWNER: {
        SpaceResourceType.ASSISTANT: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            # Note: No publish
        },
        SpaceResourceType.APP: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            # Note: No publish
        },
        SpaceResourceType.SERVICE: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            # Note: No publish
        },
        SpaceResourceType.GROUP: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            # Note: No publish
        },
        SpaceResourceType.WEBSITE: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.EDIT,
            SpaceAction.DELETE,
            # Note: No publish
        },
        SpaceResourceType.INFO_BLOB: {
            SpaceAction.READ,
            SpaceAction.CREATE,
            SpaceAction.DELETE,
        },
        SpaceResourceType.SPACE: {
            SpaceAction.READ,
        },
        SpaceResourceType.DEFAULT_ASSISTANT: {
            SpaceAction.READ,
            SpaceAction.EDIT,
        },
    },
}

PROPRIETARY_RESOURCES = {}
PERMISSION_RESOURCES = {
    SpaceResourceType.ASSISTANT,
    SpaceResourceType.APP,
    SpaceResourceType.SERVICE,
    SpaceResourceType.GROUP,
    SpaceResourceType.WEBSITE,
}
PUBLISHABLE_RESOURCES = {
    SpaceResourceType.ASSISTANT,
    SpaceResourceType.APP,
}

AccessControlList = dict[SpaceRole, dict[SpaceResourceType, set[SpaceAction]]]


# TODO: Let the services use can_perform_action()
class SpaceActor:
    def __init__(
        self,
        user: "UserInDB",
        space: "Space",
        shared_space_permissions: AccessControlList = SHARED_SPACE_PERMISSIONS,
        personal_space_permissions: AccessControlList = PERSONAL_SPACE_PERMISSIONS,
    ):
        self.user = user
        self.space = space
        self._shared_space_permissions = shared_space_permissions
        self._personal_space_permissions = personal_space_permissions

    def _to_permisson(self, resource_type: SpaceResourceType):
        permission_map = {
            SpaceResourceType.ASSISTANT: Permission.ASSISTANTS,
            SpaceResourceType.APP: Permission.APPS,
            SpaceResourceType.SERVICE: Permission.SERVICES,
            SpaceResourceType.GROUP: Permission.COLLECTIONS,
            SpaceResourceType.WEBSITE: Permission.WEBSITES,
        }

        return permission_map.get(resource_type)

    def _get_role(self):
        space_member = self.space.members.get(self.user.id)

        if self.space.is_personal():
            if self.user.id == self.space.user_id:
                return SpaceRole.OWNER

        return space_member.role if space_member else None

    def _get_permissions(self, role: SpaceRole):
        return (
            self._personal_space_permissions.get(role, {})
            if self.space.is_personal()
            else self._shared_space_permissions.get(role, {})
        )

    def can_perform_action(
        self,
        action: SpaceAction,
        resource_type: SpaceResourceType,
        resource: Union["Assistant", "App"] = None,
    ):
        role = self._get_role()
        permissions = self._get_permissions(role=role)

        if (
            not SETTINGS.using_intric_proprietary
            and resource_type in PROPRIETARY_RESOURCES
        ):
            return False

        if action == SpaceAction.PUBLISH and not SETTINGS.using_intric_proprietary:
            return False

        if (
            self.space.is_personal()
            and resource_type in PERMISSION_RESOURCES
            and self._to_permisson(resource_type=resource_type)
            not in self.user.permissions
        ):
            return False

        if (
            resource_type == SpaceResourceType.SERVICE
            and Modules.INTRIC_APPLICATIONS not in self.user.modules
        ):
            return False

        if role == SpaceRole.VIEWER and resource_type in PUBLISHABLE_RESOURCES:
            if resource is not None and not resource.published:
                return False

        allowed_actions = permissions.get(resource_type, set())
        return action in allowed_actions

    def can_read_space(self):
        return self.can_perform_action(
            action=SpaceAction.READ,
            resource_type=SpaceResourceType.SPACE,
        )

    def can_edit_space(self):
        return self.can_perform_action(
            action=SpaceAction.EDIT,
            resource_type=SpaceResourceType.SPACE,
        )

    def can_delete_space(self):
        return self.can_perform_action(
            action=SpaceAction.DELETE,
            resource_type=SpaceResourceType.SPACE,
        )

    def can_read_members(self):
        return self.can_perform_action(
            action=SpaceAction.READ,
            resource_type=SpaceResourceType.MEMBER,
        )

    def can_read_default_assistant(self):
        return self.can_perform_action(
            action=SpaceAction.READ,
            resource_type=SpaceResourceType.DEFAULT_ASSISTANT,
        )

    def can_edit_default_assistant(self):
        return self.can_perform_action(
            action=SpaceAction.EDIT,
            resource_type=SpaceResourceType.DEFAULT_ASSISTANT,
        )

    def can_read_assistants(self):
        return self.can_perform_action(
            action=SpaceAction.READ,
            resource_type=SpaceResourceType.ASSISTANT,
        )

    def can_create_assistants(self):
        return self.can_perform_action(
            action=SpaceAction.CREATE,
            resource_type=SpaceResourceType.ASSISTANT,
        )

    def can_read_assistant(self, assistant: "Assistant"):
        return self.can_perform_action(
            action=SpaceAction.READ,
            resource_type=SpaceResourceType.ASSISTANT,
            resource=assistant,
        )

    def can_edit_assistants(self):
        return self.can_perform_action(
            action=SpaceAction.EDIT,
            resource_type=SpaceResourceType.ASSISTANT,
        )

    def can_delete_assistants(self):
        return self.can_perform_action(
            action=SpaceAction.DELETE,
            resource_type=SpaceResourceType.ASSISTANT,
        )

    def can_read_prompts_of_assistants(self):
        # Considered editing an Assistant.
        # We might consider adding a separate permission
        # for this.
        return self.can_perform_action(
            action=SpaceAction.EDIT,
            resource_type=SpaceResourceType.ASSISTANT,
        )

    def can_publish_assistants(self):
        return self.can_perform_action(
            action=SpaceAction.PUBLISH,
            resource_type=SpaceResourceType.ASSISTANT,
        )

    def can_read_apps(self):
        return self.can_perform_action(
            action=SpaceAction.READ,
            resource_type=SpaceResourceType.APP,
        )

    def can_create_apps(self):
        return self.can_perform_action(
            action=SpaceAction.CREATE,
            resource_type=SpaceResourceType.APP,
        )

    def can_read_app(self, app: "App"):
        return self.can_perform_action(
            action=SpaceAction.READ,
            resource_type=SpaceResourceType.APP,
            resource=app,
        )

    def can_edit_apps(self):
        return self.can_perform_action(
            action=SpaceAction.EDIT,
            resource_type=SpaceResourceType.APP,
        )

    def can_delete_apps(self):
        return self.can_perform_action(
            action=SpaceAction.DELETE,
            resource_type=SpaceResourceType.APP,
        )

    def can_read_prompts_of_apps(self):
        # Considered editing an App.
        # We might consider adding a separate permission
        # for this.
        return self.can_perform_action(
            action=SpaceAction.EDIT,
            resource_type=SpaceResourceType.APP,
        )

    def can_publish_apps(self):
        return self.can_perform_action(
            action=SpaceAction.PUBLISH,
            resource_type=SpaceResourceType.APP,
        )

    def can_read_groups(self):
        return self.can_perform_action(
            action=SpaceAction.READ,
            resource_type=SpaceResourceType.GROUP,
        )

    def can_create_groups(self):
        return self.can_perform_action(
            action=SpaceAction.CREATE,
            resource_type=SpaceResourceType.GROUP,
        )

    def can_edit_groups(self):
        return self.can_perform_action(
            action=SpaceAction.EDIT,
            resource_type=SpaceResourceType.GROUP,
        )

    def can_delete_groups(self):
        return self.can_perform_action(
            action=SpaceAction.DELETE,
            resource_type=SpaceResourceType.GROUP,
        )

    def can_read_websites(self):
        return self.can_perform_action(
            action=SpaceAction.READ,
            resource_type=SpaceResourceType.WEBSITE,
        )

    def can_create_websites(self):
        return self.can_perform_action(
            action=SpaceAction.CREATE,
            resource_type=SpaceResourceType.WEBSITE,
        )

    def can_edit_websites(self):
        return self.can_perform_action(
            action=SpaceAction.EDIT,
            resource_type=SpaceResourceType.WEBSITE,
        )

    def can_delete_websites(self):
        return self.can_perform_action(
            action=SpaceAction.DELETE,
            resource_type=SpaceResourceType.WEBSITE,
        )

    def can_read_info_blobs(self):
        return self.can_perform_action(
            action=SpaceAction.READ,
            resource_type=SpaceResourceType.INFO_BLOB,
        )

    def can_create_info_blobs(self):
        return self.can_perform_action(
            action=SpaceAction.CREATE,
            resource_type=SpaceResourceType.INFO_BLOB,
        )

    def can_delete_info_blobs(self):
        return self.can_perform_action(
            action=SpaceAction.DELETE,
            resource_type=SpaceResourceType.INFO_BLOB,
        )

    def can_read_services(self):
        return self.can_perform_action(
            action=SpaceAction.READ,
            resource_type=SpaceResourceType.SERVICE,
        )

    def can_create_services(self):
        return self.can_perform_action(
            action=SpaceAction.CREATE,
            resource_type=SpaceResourceType.SERVICE,
        )

    def can_edit_services(self):
        return self.can_perform_action(
            action=SpaceAction.EDIT,
            resource_type=SpaceResourceType.SERVICE,
        )

    def can_delete_services(self):
        return self.can_perform_action(
            action=SpaceAction.DELETE,
            resource_type=SpaceResourceType.SERVICE,
        )

    def _get_resource_permissions(
        self, can_edit: bool, can_delete: bool, can_publish: bool
    ):
        permissions = []

        if can_edit:
            permissions.append(ResourcePermission.EDIT)

        if can_delete:
            permissions.append(ResourcePermission.DELETE)

        if can_publish:
            permissions.append(ResourcePermission.PUBLISH)

        return permissions

    def get_assistant_permissions(self, assistant: "Assistant"):
        permissions = []

        # TODO: Getting permissions should be revisited after
        # Space is the aggregate root
        if (
            self.space.default_assistant is not None
            and assistant.id == self.space.default_assistant.id
        ):
            if self.can_read_default_assistant():
                permissions.append(ResourcePermission.READ)

            if self.can_edit_default_assistant():
                permissions.append(ResourcePermission.EDIT)

            return permissions

        return self._get_resource_permissions(
            self.can_edit_assistants(),
            self.can_delete_assistants(),
            self.can_publish_assistants(),
        )

    def get_app_permissions(self):
        return self._get_resource_permissions(
            self.can_edit_apps(),
            self.can_delete_apps(),
            self.can_publish_apps(),
        )

    def get_group_permissions(self):
        return self._get_resource_permissions(
            self.can_edit_groups(),
            self.can_delete_groups(),
            False,
        )

    def get_website_permissions(self):
        return self._get_resource_permissions(
            self.can_edit_websites(),
            self.can_delete_websites(),
            False,
        )

    def get_service_permissions(self):
        return self._get_resource_permissions(
            self.can_edit_services(), self.can_delete_services(), False
        )

    def get_available_roles(self):
        if self.space.is_personal():
            return []

        roles = [SpaceRole.ADMIN, SpaceRole.EDITOR]

        if SETTINGS.using_intric_proprietary:
            roles.append(SpaceRole.VIEWER)

        return roles
