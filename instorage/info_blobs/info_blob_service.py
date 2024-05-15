from uuid import UUID

from instorage.admin.quota_service import QuotaService
from instorage.groups.group_service import GroupService
from instorage.info_blobs.info_blob import (
    InfoBlobAdd,
    InfoBlobInDB,
    InfoBlobMetadataFilter,
    InfoBlobMetadataFilterPublic,
    InfoBlobUpdate,
)
from instorage.info_blobs.info_blob_repo import InfoBlobRepository
from instorage.main.exceptions import NotFoundException, UnauthorizedException
from instorage.users.user import UserInDB


class InfoBlobService:
    def __init__(
        self,
        *,
        repo: InfoBlobRepository,
        user: UserInDB,
        quota_service: QuotaService,
        group_service: GroupService,
    ):
        self.repo = repo
        self.group_service = group_service
        self.user = user
        self.quota_service = quota_service

    async def add_info_blob_without_validation(self, info_blob: InfoBlobAdd):
        size_of_text = await self.quota_service.add_text(info_blob.text)
        info_blob.size = size_of_text
        info_blob_in_db = await self.repo.add(info_blob)

        return info_blob_in_db

    async def add_info_blob(self, info_blob: InfoBlobAdd):
        group = await self.group_service.get_group_by_uuid(info_blob.group_id)

        if group.user_id != self.user.id:
            raise UnauthorizedException(
                "Can't add info-blobs to a group that is not yours."
            )

        return await self.add_info_blob_without_validation(info_blob)

    async def add_info_blobs(self, info_blobs: list[InfoBlobAdd]):
        return [await self.add_info_blob(blob) for blob in info_blobs]

    async def update_info_blob(self, info_blob: InfoBlobUpdate):
        # Validation check
        await self.get_by_id(info_blob.id)

        info_blob_updated = await self.repo.update(info_blob)

        return info_blob_updated

    async def get_by_id(self, id: str):
        blob = await self.repo.get(id)

        if not blob:
            raise NotFoundException("InfoBlob not found")

        if blob.user_id != self.user.id:
            raise UnauthorizedException("InfoBlob belongs to other user")

        return blob

    async def get_by_user(self, metadata_filter: InfoBlobMetadataFilter | None = None):
        info_blobs = await self.repo.get_by_user(user_id=self.user.id)

        if metadata_filter:

            def filter_func(item: InfoBlobInDB):
                filter_dict = metadata_filter.model_dump(exclude_none=True)
                item_dict = item.model_dump()
                return filter_dict.items() <= item_dict.items()

            info_blobs = list(filter(filter_func, info_blobs))

        return [blob for blob in info_blobs]

    async def get_by_filter(
        self,
        metadata_filter: InfoBlobMetadataFilterPublic,
    ):
        metadata_filter_with_user = InfoBlobMetadataFilter(
            **metadata_filter.model_dump(), user_id=self.user.id
        )
        return await self.get_by_user(metadata_filter_with_user)

    async def get_by_group(self, uuid: UUID) -> list[InfoBlobInDB]:
        group = await self.group_service.get_group_by_uuid(uuid)
        return await self.repo.get_by_group(group.id)

    async def delete(self, id: str):
        # Do validation checks
        await self.get_by_id(id)

        info_blob_deleted = await self.repo.delete(id)

        return info_blob_deleted
