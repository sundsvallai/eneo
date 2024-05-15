# MIT License

from typing import Optional

from pydantic import BaseModel

from instorage.assistants.assistant import AssistantInDBBase, AssistantPublicBase
from instorage.groups.group import GroupInDBBase, GroupPublicBase
from instorage.main.models import InDB, ModelUUID, Public
from instorage.services.service import ServiceInDBBase, ServicePublicBase
from instorage.users.user import UserInDBBase, UserPublicBase


class UserGroupBase(BaseModel):
    name: str


class UserGroupCreateRequest(UserGroupBase):
    pass


class UserGroupCreate(UserGroupBase):
    tenant_id: int


class UserGroupUpdateRequest(UserGroupBase):
    name: Optional[str] = None

    users: list[ModelUUID] = []
    assistants: list[ModelUUID] = []
    services: list[ModelUUID] = []
    groups: list[ModelUUID] = []


class UserGroupUpdate(UserGroupUpdateRequest):
    id: int


class UserGroupInDB(UserGroupBase, InDB):
    tenant_id: int

    users: list[UserInDBBase] = []
    assistants: list[AssistantInDBBase] = []
    services: list[ServiceInDBBase] = []
    groups: list[GroupInDBBase] = []


class UserGroupPublic(UserGroupBase, Public):
    users: list[UserPublicBase] = []
    assistants: list[AssistantPublicBase] = []
    services: list[ServicePublicBase] = []
    groups: list[GroupPublicBase] = []
