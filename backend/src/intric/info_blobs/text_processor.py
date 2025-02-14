from pathlib import Path
from uuid import UUID

from intric.ai_models.embedding_models.datastore.datastore import Datastore
from intric.database.database import AsyncSession
from intric.files.text import TextExtractor
from intric.info_blobs.info_blob import InfoBlobAdd
from intric.info_blobs.info_blob_service import InfoBlobService
from intric.users.user import UserInDB


class TextProcessor:
    def __init__(
        self,
        user: UserInDB,
        extractor: TextExtractor,
        datastore: Datastore,
        info_blob_service: InfoBlobService,
        session: AsyncSession,
    ):
        self.user = user
        self.extractor = extractor
        self.datastore = datastore
        self.info_blob_service = info_blob_service
        self.session = session

    async def process_file(
        self,
        *,
        filepath: Path,
        filename: str,
        mimetype: str | None = None,
        group_id: UUID | None = None,
        website_id: UUID | None = None,
    ):
        text = self.extractor.extract(filepath, mimetype)

        return await self.process_text(
            text=text, title=filename, group_id=group_id, website_id=website_id
        )

    async def process_text(
        self,
        *,
        text: str,
        title: str,
        group_id: UUID | None = None,
        website_id: UUID | None = None,
        url: str | None = None,
    ):
        info_blob_add = InfoBlobAdd(
            title=title,
            user_id=self.user.id,
            text=text,
            group_id=group_id,
            url=url,
            website_id=website_id,
            tenant_id=self.user.tenant_id,
        )

        info_blob = await self.info_blob_service.add_info_blob_without_validation(
            info_blob_add
        )
        await self.datastore.add(info_blob)
        info_blob_updated = await self.info_blob_service.update_info_blob_size(
            info_blob.id
        )

        return info_blob_updated
