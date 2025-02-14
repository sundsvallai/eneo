from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from intric.ai_models.completion_models.completion_model import (
    CompletionModelPublic,
    ModelKwargs,
)
from intric.ai_models.completion_models.completion_service import CompletionService
from intric.files.file_models import File, FileInfo, FileType
from intric.files.text import TextMimeTypes
from intric.groups.api.group_models import Group
from intric.info_blobs.info_blob import InfoBlobChunkInDBWithScore
from intric.main.exceptions import (
    BadRequestException,
    NoModelSelectedException,
    UnauthorizedException,
)
from intric.prompts.prompt import Prompt
from intric.sessions.session import SessionInDB
from intric.users.user import UserSparse
from intric.websites.website_models import WebsiteSparse

if TYPE_CHECKING:
    from intric.assistants.references import ReferencesService
    from intric.templates.assistant_template.assistant_template import AssistantTemplate


UNAUTHORIZED_EXCEPTION_MESSAGE = "Unauthorized. User has no permissions to access."


class Assistant:
    def __init__(
        self,
        id: UUID | None,
        user: UserSparse | None,
        space_id: UUID,
        completion_model: CompletionModelPublic | None,
        name: str,
        prompt: Prompt | None,
        completion_model_kwargs: ModelKwargs,
        logging_enabled: bool,
        websites: list[WebsiteSparse],
        groups: list[Group],
        attachments: list[FileInfo],
        published: bool,
        source_template: Optional["AssistantTemplate"] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
        completion_service: CompletionService | None = None,
        references_service: Optional["ReferencesService"] = None,
        is_default: bool = False,
        tool_assistants: list["Assistant"] = None,
    ):
        self.id = id
        self.user = user
        self.space_id = space_id
        self._completion_model = completion_model
        self.name = name
        self.prompt = prompt
        self.completion_model_kwargs = completion_model_kwargs
        self.logging_enabled = logging_enabled
        self._websites = websites
        self._groups = groups
        self.created_at = created_at
        self.updated_at = updated_at
        self._attachments = attachments
        self.source_template = source_template
        self.completion_service = completion_service
        self.references_service = references_service
        self.published = published
        self.is_default = is_default
        self.tool_assistants = tool_assistants or []

    def _validate_embedding_model(self, items: list[Group] | list[WebsiteSparse]):
        embedding_model_id_set = set([item.embedding_model.id for item in items])
        if len(embedding_model_id_set) != 1 or (
            self.embedding_model_id is not None
            and embedding_model_id_set.pop() != self.embedding_model_id
        ):
            raise BadRequestException(
                "All websites or groups must have the same embedding model"
            )

    def _set_groups_and_websites(
        self, groups: list[Group] | None, websites: list[WebsiteSparse] | None
    ):
        if groups is None and websites is None:
            return

        elif groups is not None and websites is not None:
            self._groups.clear()
            self._websites.clear()

            self.groups = groups
            self.websites = websites

        elif groups is not None:
            self.groups = groups

        elif websites is not None:
            self.websites = websites

    @property
    def completion_model(self):
        return self._completion_model

    @completion_model.setter
    def completion_model(self, model: CompletionModelPublic):
        if not model.can_access:
            raise UnauthorizedException(UNAUTHORIZED_EXCEPTION_MESSAGE)

        self._completion_model = model

    @property
    def embedding_model_id(self):
        if not self.websites and not self.groups:
            return None

        if self.websites:
            return self.websites[0].embedding_model.id

        if self.groups:
            return self.groups[0].embedding_model.id

    @property
    def attachments(self):
        return self._attachments

    @attachments.setter
    def attachments(self, attachments: list[FileInfo]):
        for attachment in attachments:
            if not TextMimeTypes.has_value(attachment.mimetype):
                raise BadRequestException("Attachements can only be text files")

        if sum(attachment.size for attachment in attachments) > 26214400:
            raise BadRequestException("Files too large!")

        self._attachments = attachments

    @property
    def websites(self):
        return self._websites

    @websites.setter
    def websites(self, websites: list[WebsiteSparse]):
        self._websites.clear()

        if websites:
            self._validate_embedding_model(websites)

        self._websites = websites

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, groups: list[Group]):
        self._groups.clear()

        if groups:
            self._validate_embedding_model(groups)

        self._groups = groups

    def has_knowledge(self) -> bool:
        return self.groups or self.websites

    def update(
        self,
        name: str | None = None,
        prompt: Prompt | None = None,
        completion_model: CompletionModelPublic | None = None,
        completion_model_kwargs: ModelKwargs | None = None,
        attachments: list[FileInfo] | None = None,
        logging_enabled: bool | None = None,
        groups: list[Group] | None = None,
        websites: list[WebsiteSparse] | None = None,
        published: bool | None = None,
    ):
        if name is not None:
            self.name = name

        if prompt is not None:
            self.prompt = prompt

        if completion_model is not None:
            self.completion_model = completion_model

        if completion_model_kwargs is not None:
            self.completion_model_kwargs = completion_model_kwargs

        if attachments is not None:
            self.attachments = attachments

        if logging_enabled is not None:
            self.logging_enabled = logging_enabled

        if published is not None:
            self.published = published

        self._set_groups_and_websites(groups=groups, websites=websites)

    def get_prompt_text(self):
        if self.prompt is not None:
            return self.prompt.text

        return ""

    async def get_response(
        self,
        question: str,
        model_kwargs: ModelKwargs | None = None,
        files: list[File] = [],
        info_blob_chunks: list[InfoBlobChunkInDBWithScore] = [],
        session: SessionInDB | None = None,
        stream: bool = False,
        extended_logging: bool = False,
        prompt: str | None = None,
    ):
        if self.completion_model is None:
            raise NoModelSelectedException()

        return await self.completion_service.get_response(
            text_input=question,
            files=files,
            prompt=prompt or self.get_prompt_text(),
            prompt_files=self.attachments,
            info_blob_chunks=info_blob_chunks,
            session=session,
            stream=stream,
            extended_logging=extended_logging,
            model_kwargs=model_kwargs,
        )

    async def ask(
        self,
        question: str,
        session: Optional["SessionInDB"] = None,
        files: list["File"] = [],
        stream: bool = False,
        version: int = 1,
    ):
        if any([file.file_type == FileType.IMAGE for file in files]):
            if not self.completion_model.vision:
                raise BadRequestException(
                    f"Completion model {self.completion_model.name} do not support vision."
                )

        # Fill half the context
        num_chunks = (
            self.completion_model.token_limit // 200 // 2 if version == 2 else 30
        )

        datastore_result = await self.references_service.get_references(
            question=question,
            session=session,
            groups=self.groups,
            websites=self.websites,
            num_chunks=num_chunks,
            version=version,
        )

        response = await self.completion_service.get_response(
            text_input=question,
            files=files,
            prompt=self.get_prompt_text(),
            prompt_files=self.attachments,
            info_blob_chunks=datastore_result.chunks,
            session=session,
            stream=stream,
            extended_logging=self.logging_enabled,
            model_kwargs=self.completion_model_kwargs,
            version=version,
        )

        return response, datastore_result
