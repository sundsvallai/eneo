from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from intric.ai_models.completion_models.completion_model import (
    CompletionModelFamily,
    CompletionModelPublic,
    ModelKwargs,
)
from intric.ai_models.completion_models.completion_model_adapters import (
    AzureOpenAIModelAdapter,
    ClaudeModelAdapter,
    OpenAIModelAdapter,
    VLMMModelAdapter,
)
from intric.ai_models.embedding_models.embedding_model import (
    EmbeddingModel,
    EmbeddingModelFamily,
)
from intric.ai_models.embedding_models.embedding_model_adapters import (
    InfinityAdapter,
    OpenAIEmbeddingAdapter,
)
from intric.assistants.assistant import Assistant
from intric.database.tables.assistant_table import Assistants
from intric.database.tables.groups_table import Groups
from intric.database.tables.prompts_table import Prompts
from intric.files.file_models import File
from intric.groups.api.group_models import Group
from intric.main.logging import get_logger
from intric.prompts.prompt_factory import PromptFactory
from intric.users.user import UserInDB, UserSparse
from intric.websites.website_models import WebsiteSparse, WebsiteMetadata
from intric.websites.crawl_dependencies.crawl_models import CrawlRunSparse

if TYPE_CHECKING:
    from intric.database.tables.websites_table import Websites
    from intric.files.file_models import FileInfo
    from intric.main.container.container import Container
    from intric.prompts.prompt import Prompt
    from intric.templates.assistant_template.assistant_template import AssistantTemplate
    from intric.templates.assistant_template.assistant_template_factory import (
        AssistantTemplateFactory,
    )

logger = get_logger(__name__)


class AssistantFactory:
    def __init__(
        self,
        container: "Container",
        prompt_factory: PromptFactory,
        assistant_template_factory: "AssistantTemplateFactory",
    ):
        self.container = container
        self.prompt_factory = prompt_factory
        self.assistant_template_factory = assistant_template_factory

    def _get_completion_model_adapter(self, completion_model: CompletionModelPublic):
        # Completion model adapters
        match completion_model.family.value:
            case CompletionModelFamily.OPEN_AI.value:
                return OpenAIModelAdapter(model=completion_model)
            case CompletionModelFamily.VLLM.value:
                return VLMMModelAdapter(model=completion_model)
            case CompletionModelFamily.CLAUDE.value:
                return ClaudeModelAdapter(model=completion_model)
            case CompletionModelFamily.AZURE.value:
                return AzureOpenAIModelAdapter(model=completion_model)

    def _get_embedding_model(
        self,
        groups: list[tuple[Groups, int]] = [],
        websites: list["Websites"] = [],
    ):
        for group in groups:
            return EmbeddingModel.model_validate(group[0].embedding_model)

        for website in websites:
            return EmbeddingModel.model_validate(website.embedding_model)

        # Else return None

    def _get_embedding_model_adapter(
        self,
        groups: list[tuple[Groups, int]] = [],
        websites: list["Websites"] = [],
    ):
        embedding_model = self._get_embedding_model(groups=groups, websites=websites)

        if embedding_model is None:
            return

        match embedding_model.family.value:
            case EmbeddingModelFamily.E5:
                return InfinityAdapter(model=embedding_model)
            case EmbeddingModelFamily.OPEN_AI:
                return OpenAIEmbeddingAdapter(model=embedding_model)

    def create_assistant(
        self,
        name: str,
        user: UserInDB,
        space_id: UUID,
        prompt: "Prompt" | None = None,
        completion_model: CompletionModelPublic | None = None,
        completion_model_kwargs: ModelKwargs = ModelKwargs(),
        logging_enabled: bool = False,
        attachments: list["FileInfo"] | None = None,
        groups: list["Group"] | None = None,
        template: AssistantTemplate | None = None,
        is_default: bool = False,
    ) -> Assistant:
        return Assistant(
            id=None,
            user=user,
            space_id=space_id,
            name=name,
            prompt=prompt,
            completion_model=completion_model,
            completion_model_kwargs=completion_model_kwargs,
            attachments=attachments or [],
            logging_enabled=logging_enabled,
            websites=[],
            groups=groups or [],
            published=False,
            source_template=template,
            is_default=is_default,
        )

    def create_assistant_from_db(
        self,
        assistant_in_db: Assistants,
        groups_in_db: list[tuple[Groups, int]] = [],
        prompt: Prompts | None = None,
    ) -> Assistant:
        completion_model = None
        if assistant_in_db.completion_model_id is not None:
            completion_model = CompletionModelPublic.model_validate(
                assistant_in_db.completion_model
            )

        if prompt is not None:
            prompt = self.prompt_factory.create_prompt_from_db(
                prompt_in_db=prompt, is_selected=True
            )

        attachments = [
            File(**attachment.file.to_dict())
            for attachment in assistant_in_db.attachments
        ]

        groups = [
            Group(
                **group.to_dict(),
                num_info_blobs=info_blob_count,
                embedding_model=EmbeddingModel.model_validate(group.embedding_model),
            )
            for group, info_blob_count in groups_in_db
        ]
        websites = [
            WebsiteSparse(
                **website.to_dict(),
                metadata=WebsiteMetadata(size=website.size),
                latest_crawl=CrawlRunSparse.model_validate(website.latest_crawl),
                embedding_model=EmbeddingModel.model_validate(website.embedding_model),
            )
            for website in assistant_in_db.websites
        ]
        user = UserSparse.model_validate(assistant_in_db.user)
        completion_model_kwargs = ModelKwargs.model_validate(
            assistant_in_db.completion_model_kwargs
        )

        completion_service = (
            self.container.completion_service(
                model_adapter=self._get_completion_model_adapter(completion_model)
            )
            if completion_model is not None
            else None
        )
        references_service = self.container.references_service(
            datastore__embedding_model_adapter=self._get_embedding_model_adapter(
                groups=groups_in_db, websites=assistant_in_db.websites
            )
        )

        source_template = (
            self.assistant_template_factory.create_assistant_template(
                assistant_in_db.template
            )
            if assistant_in_db.template
            else None
        )

        return Assistant(
            id=assistant_in_db.id,
            user=user,
            space_id=assistant_in_db.space_id,
            name=assistant_in_db.name,
            prompt=prompt,
            completion_model=completion_model,
            completion_model_kwargs=completion_model_kwargs,
            attachments=attachments,
            logging_enabled=assistant_in_db.logging_enabled,
            websites=websites,
            groups=groups,
            created_at=assistant_in_db.created_at,
            updated_at=assistant_in_db.updated_at,
            completion_service=completion_service,
            references_service=references_service,
            published=assistant_in_db.published,
            source_template=source_template,
            is_default=assistant_in_db.is_default,
        )
