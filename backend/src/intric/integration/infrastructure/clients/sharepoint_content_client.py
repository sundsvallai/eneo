from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple
from uuid import UUID

import aiohttp

from intric.integration.infrastructure.content_service.utils import (
    process_sharepoint_response,
)
from intric.libs.clients import BaseClient
from intric.main.logging import get_logger

logger = get_logger(__name__)

TokenRefreshCallback = Callable[[UUID], Awaitable[Dict[str, str]]]


class SharePointContentClient(BaseClient):
    def __init__(
        self,
        base_url: str,
        api_token: str,
        token_id: Optional[UUID] = None,
        token_refresh_callback: Optional[TokenRefreshCallback] = None,
    ):
        super().__init__(base_url=base_url)
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Accept": "application/json",
        }
        self.api_token = api_token
        self.token_id = token_id
        # Used to do token refresh when token is expired
        self.token_refresh_callback = token_refresh_callback

    def update_token(self, new_token: str):
        """Update the token and headers with a new token value"""
        self.api_token = new_token
        self.headers = {
            "Authorization": f"Bearer {new_token}",
            "Accept": "application/json",
        }

    async def refresh_token(self):
        """Refresh the token using the provided callback"""
        if not self.token_refresh_callback or not self.token_id:
            raise ValueError(
                "Cannot refresh token: missing token_refresh_callback or token_id"
            )

        token_data = await self.token_refresh_callback(self.token_id)
        if not token_data or "access_token" not in token_data:
            raise ValueError("Token refresh callback returned invalid token data")

        self.update_token(token_data["access_token"])
        return token_data

    async def get_sites(self) -> Dict[str, Any]:
        try:
            return await self.client.get("v1.0/sites?search=*", headers=self.headers)
        except aiohttp.ClientResponseError as e:
            if e.status == 401 and self.token_refresh_callback and self.token_id:
                logger.info(
                    "SharePoint token expired while listing sites, refreshing..."
                )
                await self.refresh_token()
                return await self.client.get(
                    "v1.0/sites?search=*", headers=self.headers
                )
            else:
                raise

    async def get_site_pages(self, site_id: str) -> Dict[str, Any]:
        try:
            endpoint = f"v1.0/sites/{site_id}/pages"
            page_data = await self.client.get(endpoint, headers=self.headers)
            return page_data

        except aiohttp.ClientResponseError as e:
            if e.status == 401 and self.token_refresh_callback and self.token_id:
                await self.refresh_token()
                page_data = await self.client.get(endpoint, headers=self.headers)
                return page_data
            else:
                logger.error(f"SharePoint API error when getting page content: {e}")
                raise

    async def get_drives(
        self, site_id: str, drive_name: str = "Documents"
    ) -> Optional[str]:
        """Get the Drive ID of a document library in a SharePoint site.

        Args:
            site_id: SharePoint site ID
            drive_name: The name of the document library (default is "Documents")

        Returns:
            The Drive ID if found, else None
        """
        try:
            endpoint = f"v1.0/sites/{site_id}/drives"
            response = await self.client.get(endpoint, headers=self.headers)

            if "value" in response:
                for drive in response["value"]:
                    if drive.get("name") == drive_name:
                        return drive.get("id")

            return None
        except aiohttp.ClientResponseError as e:
            if e.status == 401 and self.token_refresh_callback and self.token_id:
                logger.info(
                    "SharePoint token expired when getting drive ID, refreshing..."
                )
                await self.refresh_token()

                endpoint = f"v1.0/sites/{site_id}/drives"
                response = await self.client.get(endpoint, headers=self.headers)

                if "value" in response:
                    for drive in response["value"]:
                        if drive.get("name") == drive_name:
                            return drive.get("id")

                return None
            else:
                logger.error(f"Error getting drive ID: {e}")
                raise

    async def get_documents_in_drive(self, site_id: str) -> dict:
        try:
            drive_id = await self.get_drives(site_id=site_id)
            endpoint = f"v1.0/sites/{site_id}/drives/{drive_id}/root/children"
            response = await self.client.get(endpoint, headers=self.headers)
            return response
        except aiohttp.ClientResponseError as e:
            if e.status == 401 and self.token_refresh_callback and self.token_id:
                logger.info("SharePoint token expired, refreshing...")
                await self.refresh_token()

                drive_id = await self.get_drives(site_id=site_id)
                endpoint = f"v1.0/sites/{site_id}/drives/{drive_id}/root/children"
                response = await self.client.get(endpoint, headers=self.headers)
                return response
            else:
                logger.error(f"SharePoint API error: {e}")
                raise

    async def get_file_metadata(self, drive_id: str, item_id: str) -> Dict[str, Any]:
        """
        Get metadata for a SharePoint item (file or folder) by its ID.

        Args:
            drive_id: The ID of the drive containing the item
            item_id: The ID of the item

        Returns:
            Dictionary containing the item's metadata
        """
        try:
            endpoint = f"v1.0/drives/{drive_id}/items/{item_id}"
            return await self.client.get(endpoint, headers=self.headers)
        except aiohttp.ClientResponseError as e:
            if e.status == 401 and self.token_refresh_callback and self.token_id:
                logger.info(
                    "SharePoint token expired while getting file metadata, refreshing..."
                )
                await self.refresh_token()

                endpoint = f"v1.0/drives/{drive_id}/items/{item_id}"
                return await self.client.get(endpoint, headers=self.headers)
            else:
                logger.error(f"SharePoint API error when getting file metadata: {e}")
                raise

    async def get_folder_items(
        self,
        site_id: str,
        drive_id: str,
        folder_id: str,
    ) -> List[Dict[str, Any]]:
        """Get items in a folder or the root of a drive.

        Args:
            site_id: The SharePoint site ID
            drive_id: The drive ID
            folder_id: The folder ID

        Returns:
            List of items in the folder
        """
        try:
            endpoint = (
                f"v1.0/sites/{site_id}/drives/{drive_id}/items/{folder_id}/children"
            )
            response = await self.client.get(endpoint, headers=self.headers)
            return response.get("value", [])
        except aiohttp.ClientResponseError as e:
            if e.status == 401 and self.token_refresh_callback and self.token_id:
                logger.info(
                    "SharePoint token expired while getting folder items, refreshing..."
                )
                await self.refresh_token()
                endpoint = (
                    f"v1.0/sites/{site_id}/drives/{drive_id}/items/{folder_id}/children"
                )
                response = await self.client.get(endpoint, headers=self.headers)
                return response.get("value", [])
            else:
                logger.error(f"SharePoint API error while getting folder items: {e}")
                raise

    async def get_page_content(self, site_id: str, page_id: str) -> Dict[str, Any]:
        try:
            endpoint = f"v1.0/sites/{site_id}/pages/{page_id}/microsoft.graph.sitePage?$expand=canvasLayout"  # noqa E501
            page_data = await self.client.get(endpoint, headers=self.headers)
            return page_data

        except aiohttp.ClientResponseError as e:
            if e.status == 401 and self.token_refresh_callback and self.token_id:
                page_data = await self.client.get(endpoint, headers=self.headers)
                return page_data
            else:
                logger.error(f"SharePoint API error when getting page content: {e}")
                raise

    async def get_file_content_by_id(
        self, drive_id: str, item_id: str
    ) -> Tuple[str, str]:
        """
        Get the content of a file by its ID.

        Args:
            drive_id: The ID of the drive containing the file
            item_id: The ID of the file

        Returns:
            Tuple of (extracted text, content type)
        """
        try:
            file_info = await self.get_file_metadata(drive_id, item_id)
            file_name = file_info.get("name", "")

            download_url = file_info.get("@microsoft.graph.downloadUrl")
            if not download_url:
                return "[Error: No download URL available]", "text/plain"

            async with self.client.client.get(
                download_url, headers=self.headers
            ) as response:
                response.raise_for_status()
                content_type = response.headers.get("Content-Type", "")

                if "application/json" in content_type:
                    data = await response.json()
                    return str(data), content_type
                elif "text/" in content_type or content_type == "application/xml":
                    return await response.text(), content_type
                else:
                    binary_content = await response.read()
                    text, detected_content_type = process_sharepoint_response(
                        response_content=binary_content,
                        content_type=content_type,
                        filename=file_name,
                    )
                    return text, detected_content_type
        except aiohttp.ClientResponseError as e:
            if e.status == 401 and self.token_refresh_callback and self.token_id:
                logger.info(
                    "SharePoint token expired while getting file content, refreshing..."
                )
                await self.refresh_token()

                file_info = await self.get_file_metadata(drive_id, item_id)
                file_name = file_info.get("name", "")

                download_url = file_info.get("@microsoft.graph.downloadUrl")
                if not download_url:
                    return (
                        "[Error: No download URL available after token refresh]",
                        "text/plain",
                    )

                url = download_url
                async with self.client.client.get(
                    url, headers=self.headers
                ) as response:
                    response.raise_for_status()
                    content_type = response.headers.get("Content-Type", "")

                    if "application/json" in content_type:
                        data = await response.json()
                        return str(data), content_type
                    elif "text/" in content_type or content_type == "application/xml":
                        return await response.text(), content_type
                    else:
                        binary_content = await response.read()
                        text, detected_content_type = process_sharepoint_response(
                            response_content=binary_content,
                            content_type=content_type,
                            filename=file_name,
                        )
                        return text, detected_content_type
            else:
                logger.error(f"SharePoint API error when getting file content: {e}")
                raise
