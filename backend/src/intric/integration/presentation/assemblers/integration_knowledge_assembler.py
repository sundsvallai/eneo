from typing import TYPE_CHECKING

from intric.ai_models.embedding_models.embedding_model import (
    EmbeddingModelPublicLegacy,
)
from intric.integration.presentation.models import (
    IntegrationKnowledgeMetaData,
    IntegrationKnowledgePublic,
)
from intric.jobs.job_models import Task

if TYPE_CHECKING:
    from intric.integration.domain.entities.integration_knowledge import (
        IntegrationKnowledge,
    )


class IntegrationKnowledgeAssembler:
    @classmethod
    def to_space_knowledge_model(
        cls,
        item: "IntegrationKnowledge",
    ) -> IntegrationKnowledgePublic:
        embedding_model = EmbeddingModelPublicLegacy.model_validate(item.embedding_model)
        integration_type = item.user_integration.tenant_integration.integration.integration_type

        if integration_type == "confluence":
            task = Task.PULL_CONFLUENCE_CONTENT
        elif integration_type == "sharepoint":
            task = Task.PULL_SHAREPOINT_CONTENT
        else:
            raise ValueError("Unknown integration type")
        return IntegrationKnowledgePublic(
            id=item.id,
            name=item.name,
            url=item.url,
            tenant_id=item.tenant_id,
            space_id=item.space_id,
            user_integration_id=item.user_integration.id,
            embedding_model=embedding_model,
            permissions=getattr(item, "permissions", []),
            metadata=IntegrationKnowledgeMetaData(size=item.size),
            integration_type=integration_type,
            task=task,
        )

    @classmethod
    def to_knowledge_model_list(
        cls, items: list["IntegrationKnowledge"]
    ) -> list[IntegrationKnowledgePublic]:
        return [cls.to_space_knowledge_model(i) for i in items]
