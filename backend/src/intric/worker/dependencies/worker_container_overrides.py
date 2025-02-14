from uuid import UUID

from intric.main.container.container import Container
from intric.main.container.container_overrides import override_embedding_model


async def override_embedding_model_from_group(container: Container, group_id: UUID):
    group = await container.group_repo().get_group(group_id)
    override_embedding_model(container=container, embedding_model=group.embedding_model)


async def override_embedding_model_from_website(
    container: Container, website_id: UUID, tenant_id: UUID
):
    website = await container.website_repo().get(website_id)
    embedding_model = await container.embedding_model_repo().get_model(
        id=website.embedding_model_id, tenant_id=tenant_id
    )
    override_embedding_model(container=container, embedding_model=embedding_model)
