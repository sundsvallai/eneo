from pathlib import Path
from uuid import UUID

from instorage.ai_models.embedding_models.datastore.datastore import Datastore
from instorage.database.database import AsyncSession
from instorage.info_blobs.file.text import TextExtractor
from instorage.info_blobs.info_blob import InfoBlobAdd
from instorage.info_blobs.info_blob_service import InfoBlobService
from instorage.users.user import UserInDB


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

    async def process_file(self, *, filepath: Path, filename: str, group_id: UUID):
        text = await self.extractor.extract(filepath)

        return await self.process_text(text=text, title=filename, group_id=group_id)

    async def process_text(
        self, *, text: str, title: str, group_id: UUID, url: str = None
    ):
        info_blob_add = InfoBlobAdd(
            title=title, user_id=self.user.id, text=text, group_id=group_id, url=url
        )

        async with self.session.begin():
            info_blob = await self.info_blob_service.add_info_blob_without_validation(
                info_blob_add
            )
            await self.datastore.add(info_blob)

            return info_blob
