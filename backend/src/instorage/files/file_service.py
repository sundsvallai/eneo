# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

from uuid import UUID

from fastapi import UploadFile

from instorage.files.file_models import FileCreate
from instorage.files.file_protocol import FileProtocol
from instorage.files.file_repo import FileRepository
from instorage.main.exceptions import UnauthorizedException
from instorage.main.models import ModelId
from instorage.users.user import UserInDB


class FileService:
    def __init__(self, user: UserInDB, repo: FileRepository, protocol: FileProtocol):
        self.user = user
        self.repo = repo
        self.protocol = protocol

    async def save_file(self, upload_file: UploadFile):
        file = await self.protocol.to_domain(upload_file)

        return await self.repo.add(
            FileCreate(
                **file.model_dump(),
                user_id=self.user.id,
                tenant_id=self.user.tenant_id,
            )
        )

    async def get_files_by_ids(self, file_ids: list[ModelId]):
        return await self.repo.get_list_by_id_and_user(
            ids=[file_id.id for file_id in file_ids], user_id=self.user.id
        )

    async def get_files(self):
        return await self.repo.get_list_by_user(user_id=self.user.id)

    async def delete_file(self, id: UUID):
        file_deleted = await self.repo.delete(id)

        if file_deleted.user_id != self.user.id:
            raise UnauthorizedException()

        return file_deleted
