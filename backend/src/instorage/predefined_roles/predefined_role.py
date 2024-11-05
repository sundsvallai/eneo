# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from instorage.main.models import DateTimeModelMixin
from instorage.roles.permissions import Permission


class PredefinedRoleBase(BaseModel):
    name: str
    permissions: list[Permission]


class PredefinedRoleCreate(PredefinedRoleBase):
    pass


class PredefinedRoleUpdateRequest(PredefinedRoleBase):
    name: Optional[str] = None
    permissions: Optional[list[Permission]] = None


class PredefinedRoleUpdate(PredefinedRoleUpdateRequest):
    id: UUID


class PredefinedRoleInDB(PredefinedRoleBase, DateTimeModelMixin):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class PredefinedRolePublic(PredefinedRoleInDB):
    pass
