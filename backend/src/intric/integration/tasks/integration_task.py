from typing import TYPE_CHECKING

from intric.main.models import ChannelType
from intric.worker.worker import Worker

if TYPE_CHECKING:
    from intric.integration.presentation.models import (
        ConfluenceContentTaskParam,
        SharepointContentTaskParam,
    )
    from intric.main.container.container import Container

worker = Worker()


@worker.task(channel_type=ChannelType.PULL_CONFLUENCE_CONTENT)
async def pull_confluence_content(
    params: "ConfluenceContentTaskParam", container: "Container", **kw
):
    knowledge = await container.integration_knowledge_repo().one(id=params.integration_knowledge_id)

    service = container.confluence_content_service()

    await service.pull_content(
        token_id=params.token_id,
        space_key=params.space_key,
        integration_knowledge_id=knowledge.id,
    )


@worker.task(channel_type=ChannelType.PULL_SHAREPOINT_CONTENT)
async def pull_sharepoint_content(
    params: "SharepointContentTaskParam", container: "Container", **kw
):
    knowledge = await container.integration_knowledge_repo().one(id=params.integration_knowledge_id)

    service = container.sharepoint_content_service()

    await service.pull_content(
        token_id=params.token_id,
        integration_knowledge_id=knowledge.id,
        site_id=params.site_id,
    )
