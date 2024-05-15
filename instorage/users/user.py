import string
from typing import Optional

from pydantic import ConfigDict, EmailStr, Field, computed_field, field_validator

from instorage.authentication.auth_models import (
    AccessToken,
    ApiKey,
    ApiKeyInDB,
    OIDCProviders,
)
from instorage.main.models import BaseModel, InDB, ModelUUID, Public
from instorage.predefined_roles.predefined_role import (
    PredefinedRoleInDB,
    PredefinedRolePublic,
)
from instorage.roles.permissions import Permission
from instorage.roles.role import RoleInDB, RolePublic
from instorage.tenants.tenant import TenantInDB

ALLOWED_CHARS = string.ascii_letters + string.digits + "-" + "_"


class UserBase(BaseModel):
    """
    Leaving off password and salt from base model
    """

    email: EmailStr
    username: str

    @field_validator("username")
    def username_is_valid(cls, username: str) -> str:
        if not all(char in ALLOWED_CHARS for char in username):
            raise ValueError("Invalid characters in username")
        if len(username) < 3:
            raise ValueError("Username must be 3 characters or more")

        return username


class UserAdd(UserBase):
    """
    Email, username, and password are required for registering a new user
    """

    id: Optional[int] = None
    password: str = Field(min_length=7, max_length=100)
    salt: str
    used_tokens: int = 0
    email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False
    tenant_id: int
    quota_limit: Optional[int] = None
    created_with: Optional[OIDCProviders] = None

    roles: list[ModelUUID] = []
    predefined_roles: list[ModelUUID] = []


class UserUpdate(UserBase):
    id: int
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=7, max_length=100)
    used_tokens: Optional[int] = None
    email_verified: Optional[bool] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    tenant_id: Optional[int] = None
    quota_limit: Optional[int] = None
    salt: Optional[str] = None

    roles: Optional[list[ModelUUID]] = None
    predefined_roles: list[ModelUUID] = None


class UserInDBBase(InDB, UserAdd):
    """
    Add in created_at, updated_at
    """

    roles: list[RoleInDB] = []
    predefined_roles: list[PredefinedRoleInDB] = []

    model_config = ConfigDict(from_attributes=True)


class UserGroupInDBRead(InDB):
    name: str


class UserGroupRead(Public):
    name: str


class UserInDB(UserInDBBase):
    user_groups: list[UserGroupInDBRead] = []
    tenant: TenantInDB
    api_key: Optional[ApiKeyInDB] = None

    @computed_field
    @property
    def modules(self) -> list[str]:
        return [module.name for module in self.tenant.modules]

    @computed_field
    @property
    def user_groups_ids(self) -> set[int]:
        return {user_group.id for user_group in self.user_groups}

    @computed_field
    @property
    def permissions(self) -> set[Permission]:
        permissions_set = set()

        # Add permissions from roles
        for role in self.roles:
            permissions_set.update(role.permissions)

        # Add permissions from predefined roles
        for predefined_role in self.predefined_roles:
            permissions_set.update(predefined_role.permissions)

        return permissions_set


class UserCreated(UserInDB):
    access_token: Optional[AccessToken]
    api_key: Optional[ApiKey]
    roles: list[RoleInDB] = []
    predefined_roles: list[PredefinedRoleInDB] = []


class UserPublicBase(Public, UserBase):
    pass


class UserPublic(UserPublicBase):
    truncated_api_key: Optional[str] = None
    is_superuser: bool
    quota_limit: Optional[int] = None
    roles: list[RolePublic]
    predefined_roles: list[PredefinedRolePublic]
    user_groups: list[UserGroupRead]


class UserPublicWithAccessToken(UserPublic):
    access_token: AccessToken


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=7, max_length=100)


class UserAddAdmin(UserLogin, UserBase):
    is_superuser: bool = False
    quota_limit: Optional[int] = Field(
        description="Size in bytes", ge=1e3, default=None
    )
    created_with: Optional[OIDCProviders] = Field(
        description="If intended to be used with a Open ID Provider", default=None
    )

    roles: list[ModelUUID] = []
    predefined_roles: list[ModelUUID] = []


class UserAddSuperAdmin(UserAddAdmin):
    tenant_id: int


class UserAdminView(UserPublicBase):
    used_tokens: int
    email_verified: bool
    is_superuser: bool
    quota_limit: Optional[int]
    created_with: Optional[OIDCProviders]

    roles: list[RolePublic]
    predefined_roles: list[PredefinedRolePublic]
    user_groups: list[UserGroupRead]


class UserCreatedAdminView(UserAdminView):
    api_key: ApiKey


class UserUpdatePublic(UserBase):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=7, max_length=100)
    quota_limit: Optional[int] = Field(
        description="Size in bytes", ge=1e3, default=None
    )
    is_superuser: Optional[bool] = None
    roles: Optional[list[ModelUUID]] = None
    predefined_roles: list[ModelUUID] = None
