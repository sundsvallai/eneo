# MIT License

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from instorage.main.exceptions import UnauthorizedException

if TYPE_CHECKING:
    from instorage.users.user import UserInDB


class Permission(str, Enum):
    ASSISTANTS = "assistants"
    SERVICES = "services"
    COLLECTIONS = "collections"
    INSIGHTS = "insights"
    AI = "AI"
    COMPLIANCE = "compliance"
    DEPLOYER = "deployer"
    EDITOR = "editor"
    ADMIN = "admin"


def validate_permissions(permission: Permission):
    """This decorator can only be used on class methods
    where a user exists in the `self`.
    """

    def _validate(func):
        async def _inner(self, *args, **kwargs):
            if permission not in self.user.permissions:
                raise UnauthorizedException(
                    f"Need permission {permission.value} in order to access"
                )

            return await func(self, *args, **kwargs)

        return _inner

    return _validate


def validate_permission(user: UserInDB, permission: Permission):
    if permission not in user.permissions:
        raise UnauthorizedException(
            f"Need permission {permission.value} in order to access"
        )
