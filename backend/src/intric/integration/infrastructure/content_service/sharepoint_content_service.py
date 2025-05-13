from typing import TYPE_CHECKING, Any, Dict, List, Optional
from uuid import UUID

from intric.embedding_models.infrastructure.datastore import Datastore
from intric.info_blobs.info_blob import InfoBlobAdd
from intric.integration.domain.entities.oauth_token import SharePointToken
from intric.integration.infrastructure.clients.sharepoint_content_client import (
    SharePointContentClient,
)
from intric.integration.infrastructure.content_service.utils import (
    file_extension_to_type,
)
from intric.main.logging import get_logger

if TYPE_CHECKING:
    from intric.database.database import AsyncSession
    from intric.info_blobs.info_blob_service import InfoBlobService
    from intric.integration.domain.entities.integration_knowledge import (
        IntegrationKnowledge,
    )
    from intric.integration.domain.repositories.integration_knowledge_repo import (
        IntegrationKnowledgeRepository,
    )
    from intric.integration.domain.repositories.oauth_token_repo import (
        OauthTokenRepository,
    )
    from intric.integration.domain.repositories.user_integration_repo import (
        UserIntegrationRepository,
    )
    from intric.integration.infrastructure.oauth_token_service import (
        OauthTokenService,
    )
    from intric.jobs.job_service import JobService
    from intric.users.user import UserInDB


logger = get_logger(__name__)


class SharePointContentService:
    def __init__(
        self,
        job_service: "JobService",
        oauth_token_repo: "OauthTokenRepository",
        user_integration_repo: "UserIntegrationRepository",
        user: "UserInDB",
        datastore: "Datastore",
        info_blob_service: "InfoBlobService",
        integration_knowledge_repo: "IntegrationKnowledgeRepository",
        oauth_token_service: "OauthTokenService",
        session: "AsyncSession",
    ):
        self.job_service = job_service
        self.oauth_token_repo = oauth_token_repo
        self.user_integration_repo = user_integration_repo
        self.user = user
        self.datastore = datastore
        self.info_blob_service = info_blob_service
        self.integration_knowledge_repo = integration_knowledge_repo
        self.oauth_token_service = oauth_token_service
        self.session = session

    async def pull_content(
        self,
        token_id: UUID,
        integration_knowledge_id: UUID,
        site_id: str,
    ):
        token = await self.oauth_token_repo.one(id=token_id)
        await self._pull_content(
            token=token,
            integration_knowledge_id=integration_knowledge_id,
            site_id=site_id,
        )

    async def _pull_content(
        self,
        token: "SharePointToken",
        integration_knowledge_id: UUID,
        site_id: str,
    ):
        """
        Process a document by its ID. First checks if it's a file or folder,
        then processes accordingly.

        Args:
            token: SharePoint token for authentication
            integration_knowledge_id: ID of the integration knowledge object
            site_id: The SharePoint site ID to process
        """
        integration_knowledge = await self.integration_knowledge_repo.one(
            id=integration_knowledge_id
        )

        try:
            async with SharePointContentClient(
                base_url=token.base_url,
                api_token=token.access_token,
                token_id=token.id,
                token_refresh_callback=self.token_refresh_callback,
            ) as content_client:
                # Documents, include folders
                documents = await content_client.get_documents_in_drive(site_id=site_id)
                if data := documents.get("value", []):
                    await self._process_documents(
                        documents=data,
                        client=content_client,
                        integration_knowledge=integration_knowledge,
                        token=token,
                    )

                # Site pages
                pages = await content_client.get_site_pages(site_id=site_id)
                if data := pages.get("value", []):
                    await self._process_pages(
                        pages=data,
                        client=content_client,
                        integration_knowledge=integration_knowledge,
                    )

        except Exception as e:
            logger.error(f"Error processing document {site_id}: {e}")
            raise

    async def _process_documents(
        self,
        documents: list[dict],
        client: SharePointContentClient,
        integration_knowledge: "IntegrationKnowledge",
        token: "SharePointToken",
    ):
        for document in documents:
            drive_id = document.get("parentReference", {}).get("driveId")
            site_id = document.get("parentReference", {}).get("siteId")
            item_id = document.get("id")
            if document.get("folder", {}):
                # Recursively process all items in the folder
                processed_items = set()
                await self._fetch_and_process_content(
                    site_id=site_id,
                    drive_id=drive_id,
                    client=client,
                    token=token,
                    integration_knowledge_id=integration_knowledge.id,
                    folder_id=item_id,
                    processed_items=processed_items,
                )
            else:
                # file
                content, _ = await client.get_file_content_by_id(drive_id=drive_id, item_id=item_id)
                if content:
                    await self._process_info_blob(
                        title=document.get("name", ""),
                        text=content,
                        url=document.get("webUrl", ""),
                        integration_knowledge=integration_knowledge,
                    )

    async def _process_pages(
        self,
        pages: list,
        client: SharePointContentClient,
        integration_knowledge: "IntegrationKnowledge",
    ):
        for page in pages:
            site_id = page.get("parentReference", {}).get("siteId")
            content = await client.get_page_content(site_id=site_id, page_id=page.get("id"))
            if content:
                await self._process_info_blob(
                    title=content.get("title", ""),
                    text=content.get("description", ""),
                    url=content.get("webUrl", ""),
                    integration_knowledge=integration_knowledge,
                )

    async def _process_info_blob(
        self,
        title: str,
        text: str,
        url: str,
        integration_knowledge: "IntegrationKnowledge",
    ) -> None:
        integration_knowledge_size = integration_knowledge.size
        info_blob_add = InfoBlobAdd(
            title=title,
            user_id=self.user.id,
            text=text,
            group_id=None,
            url=url,
            website_id=None,
            tenant_id=self.user.tenant_id,
            integration_knowledge_id=integration_knowledge.id,
        )

        info_blob = await self.info_blob_service.add_info_blob_without_validation(info_blob_add)
        await self.datastore.add(
            info_blob=info_blob, embedding_model=integration_knowledge.embedding_model
        )

        integration_knowledge_size += info_blob.size
        integration_knowledge.size = integration_knowledge_size
        await self.integration_knowledge_repo.update(obj=integration_knowledge)

    async def _fetch_and_process_content(
        self,
        site_id: str,
        drive_id: str,
        token: "SharePointToken",
        integration_knowledge_id: UUID,
        client: SharePointContentClient,
        folder_id: Optional[str] = None,
        processed_items: set = None,
    ):
        if processed_items is None:
            processed_items = set()

        results = await client.get_folder_items(
            site_id=site_id, drive_id=drive_id, folder_id=folder_id
        )

        if not results:
            return

        await self._process_folder_results(
            site_id=site_id,
            drive_id=drive_id,
            client=client,
            results=results,
            integration_knowledge_id=integration_knowledge_id,
            token=token,
            processed_items=processed_items,
        )

    async def _process_folder_results(
        self,
        site_id: str,
        drive_id: str,
        client: SharePointContentClient,
        results: List[Dict[str, Any]],
        integration_knowledge_id: UUID,
        token: "SharePointToken",
        processed_items: set,
    ) -> None:
        integration_knowledge = await self.integration_knowledge_repo.one(
            id=integration_knowledge_id
        )
        integration_knowledge_size = integration_knowledge.size

        for item in results:
            item_id = item.get("id")

            if item_id in processed_items:
                continue

            processed_items.add(item_id)

            item_name = item.get("name", "")
            item_type = self._get_item_type(item)
            web_url = item.get("webUrl", "")

            if item_type == "folder":
                await self._fetch_and_process_content(
                    site_id=site_id,
                    drive_id=drive_id,
                    client=client,
                    token=token,
                    integration_knowledge_id=integration_knowledge_id,
                    folder_id=item_id,
                    processed_items=processed_items,
                )
                continue

            content = await self._get_file_content(token, item)

            if content:
                async with self.session.begin_nested():
                    info_blob_add = InfoBlobAdd(
                        title=item_name,
                        user_id=self.user.id,
                        text=content,
                        group_id=None,
                        url=web_url,
                        website_id=None,
                        tenant_id=self.user.tenant_id,
                        integration_knowledge_id=integration_knowledge_id,
                    )

                    info_blob = await self.info_blob_service.add_info_blob_without_validation(
                        info_blob_add
                    )
                    await self.datastore.add(
                        info_blob=info_blob, embedding_model=integration_knowledge.embedding_model
                    )

                    integration_knowledge_size += info_blob.size

        integration_knowledge.size = integration_knowledge_size
        await self.integration_knowledge_repo.update(obj=integration_knowledge)

    async def token_refresh_callback(self, token_id: UUID) -> Dict[str, str]:
        token = await self.oauth_token_service.refresh_and_update_token(token_id=token_id)
        return {
            "access_token": token.access_token,
            "refresh_token": token.refresh_token,
        }

    def _get_item_type(self, item: Dict[str, Any]) -> str:
        if item.get("folder"):
            return "folder"

        return file_extension_to_type(item.get("name", ""))

    async def _get_file_content(
        self, token: "SharePointToken", item: Dict[str, Any]
    ) -> Optional[str]:
        item_id = item.get("id")
        item_name = item.get("name", "").lower()
        item_type = self._get_item_type(item)
        drive_id = item.get("parentReference", {}).get("driveId")

        if not item_id or item_type == "folder" or not drive_id:
            return None

        try:
            async with SharePointContentClient(
                base_url=token.base_url,
                api_token=token.access_token,
                token_id=token.id,
                token_refresh_callback=self.token_refresh_callback,
            ) as content_client:
                content, _ = await content_client.get_file_content_by_id(
                    drive_id=drive_id, item_id=item_id
                )
                return content

        except Exception as e:
            logger.error(f"Error getting file content for {item_name}: {e}")
            return
