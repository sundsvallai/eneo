from typing import Optional
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
from instorage.main.exceptions import NameCollisionException, NotFoundException
from instorage.main.logging import get_logger
from instorage.spaces.space import SpacePermissionsActions
from instorage.users.user import UserInDB
from instorage.websites.website_service import WebsiteService

logger = get_logger(__name__)


class InfoBlobService:
    def __init__(
        self,
        *,
        repo: InfoBlobRepository,
        user: UserInDB,
        quota_service: QuotaService,
        group_service: GroupService,
        website_service: WebsiteService,
    ):
        self.repo = repo
        self.group_service = group_service
        self.website_service = website_service
        self.user = user
        self.quota_service = quota_service

    async def _validate(
        self,
        info_blob: Optional[InfoBlobInDB],
        action: SpacePermissionsActions = SpacePermissionsActions.READ,
    ):
        if info_blob is None:
            raise NotFoundException("InfoBlob not found")

        if info_blob.group_id is not None:
            group = await self.group_service.get_group(info_blob.group_id)
            await self.group_service.check_permissions(group=group, action=action)

        elif info_blob.website_id is not None:
            website = await self.website_service.get_website(info_blob.website_id)
            await self.website_service.check_permissions(website=website, action=action)

        # Else this is a rogue info-blob
        # Be free

    async def delete_if_same_title(self, info_blob: InfoBlobAdd):
        # Only replace when uploading from group
        if info_blob.title and info_blob.group_id:
            info_blob_deleted = await self.repo.delete_by_title_and_group(
                info_blob.title, info_blob.group_id
            )

            if info_blob_deleted is not None:
                logger.info(
                    f"Info blob ({info_blob_deleted.title}) in group "
                    f"({info_blob.group_id}) was replaced"
                )

    async def add_info_blob_without_validation(self, info_blob: InfoBlobAdd):
        await self.delete_if_same_title(info_blob)
        size_of_text = await self.quota_service.add_text(info_blob.text)
        info_blob.size = size_of_text
        info_blob_in_db = await self.repo.add(info_blob)

        return info_blob_in_db

    async def add_info_blob(self, info_blob: InfoBlobAdd):
        info_blob_in_db = await self.add_info_blob_without_validation(info_blob)

        await self._validate(info_blob_in_db)

        return info_blob_in_db

    async def add_info_blobs(self, info_blobs: list[InfoBlobAdd]):
        return [await self.add_info_blob(blob) for blob in info_blobs]

    async def update_info_blob(self, info_blob: InfoBlobUpdate):
        current_info_blob = await self.repo.get(info_blob.id)

        if info_blob.title:
            info_blob_with_same_name = await self.repo.get_by_title_and_group(
                info_blob.title, current_info_blob.group.id
            )

            if info_blob_with_same_name is not None:
                raise NameCollisionException(
                    "Info blob with same name already exists in the same group"
                )

        info_blob_updated = await self.repo.update(info_blob)

        await self._validate(info_blob_updated, action=SpacePermissionsActions.EDIT)

        return info_blob_updated

    async def get_by_id(self, id: str):
        blob = await self.repo.get(id)

        await self._validate(blob)

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

    async def get_by_group(self, id: UUID) -> list[InfoBlobInDB]:
        group = await self.group_service.get_group(id)
        return await self.repo.get_by_group(group.id)

    async def get_by_website(self, id: UUID) -> list[InfoBlobInDB]:
        website = await self.website_service.get_website(id)
        return await self.repo.get_by_website(website.id)

    async def delete(self, id: str):
        info_blob_deleted = await self.repo.delete(id)

        await self._validate(info_blob_deleted, action=SpacePermissionsActions.DELETE)

        return info_blob_deleted
