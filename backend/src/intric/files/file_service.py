from uuid import UUID

from fastapi import UploadFile

from intric.files.file_models import FileCreate
from intric.files.file_protocol import FileProtocol
from intric.files.file_repo import FileRepository
from intric.main.exceptions import UnauthorizedException
from intric.users.user import UserInDB


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

    async def get_file_by_id(self, file_id: UUID):
        file = await self.repo.get_by_id(file_id=file_id)
        if file.user_id != self.user.id:
            raise UnauthorizedException()
        return file

    async def get_files_by_ids(self, file_ids: list[UUID]):
        return await self.repo.get_list_by_id_and_user(
            ids=file_ids, user_id=self.user.id
        )

    async def get_files(self):
        return await self.repo.get_list_by_user(user_id=self.user.id)

    async def get_file_infos(self, file_ids: list[UUID]):
        files = await self.repo.get_file_infos(file_ids)

        for file in files:
            if file.user_id != self.user.id:
                raise UnauthorizedException()

        return files

    async def delete_file(self, id: UUID):
        file_deleted = await self.repo.delete(id)

        if file_deleted.user_id != self.user.id:
            raise UnauthorizedException()

        return file_deleted
