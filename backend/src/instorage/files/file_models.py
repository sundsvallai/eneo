# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, model_validator

from instorage.main.models import InDB


class FileType(str, Enum):
    TEXT = "text"
    IMAGE = "image"


class FileBase(BaseModel):
    name: str
    text: Optional[str] = None
    image: Optional[bytes] = None
    checksum: str
    size: int
    mimetype: Optional[str] = None

    file_type: FileType

    @model_validator(mode="after")
    def require_one_of_text_or_image(self) -> "FileCreate":
        if self.text is None and self.image is None:
            raise ValueError("One of 'text' or 'image' is required")

        return self


class FileCreate(FileBase):
    user_id: UUID
    tenant_id: UUID


class File(InDB, FileCreate):
    pass


class FilePublic(InDB):
    name: str
    mimetype: str
    size: int
