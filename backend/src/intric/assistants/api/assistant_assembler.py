from typing import TYPE_CHECKING

from intric.assistants.api.assistant_models import AssistantPublic, DefaultAssistant
from intric.assistants.assistant import Assistant
from intric.files.file_models import (
    AcceptedFileType,
    FilePublic,
    FileRestrictions,
    Limit,
)
from intric.files.text import TextMimeTypes
from intric.groups.api.group_protocol import to_group_public_with_metadata
from intric.prompts.api.prompt_assembler import PromptAssembler
from intric.questions.question import ToolAssistant, Tools
from intric.users.user import UserInDB

if TYPE_CHECKING:
    from intric.main.models import ResourcePermission


class AssistantAssembler:
    def __init__(self, user: UserInDB, prompt_assembler: PromptAssembler):
        self.user = user
        self.prompt_assembler = prompt_assembler

    def _get_prompt(self, assistant: Assistant):
        return (
            self.prompt_assembler.from_prompt_to_model(assistant.prompt)
            if assistant.prompt
            else None
        )

    def _get_attachments(self, assistant: Assistant):
        return [
            FilePublic(**attachment.model_dump())
            for attachment in assistant.attachments
        ]

    def _get_allowed_attachments(self):
        return FileRestrictions(
            accepted_file_types=[
                AcceptedFileType(mimetype=mimetype, size_limit=26214400)
                for mimetype in TextMimeTypes.values()
            ],
            limit=Limit(max_files=3, max_size=26214400),
        )

    def from_assistant_to_model(
        self,
        assistant: Assistant,
        permissions: list["ResourcePermission"] = None,
    ):
        permissions = permissions or []

        prompt = self._get_prompt(assistant)
        attachments = self._get_attachments(assistant)
        allowed_attachments = self._get_allowed_attachments()
        tools = Tools(
            assistants=[
                ToolAssistant(id=tool_assistant.id, at_tag=tool_assistant.name)
                for tool_assistant in assistant.tool_assistants
            ]
        )

        groups = [
            to_group_public_with_metadata(
                group=group, num_info_blobs=group.num_info_blobs
            )
            for group in assistant.groups
        ]

        return AssistantPublic(
            created_at=assistant.created_at,
            updated_at=assistant.updated_at,
            id=assistant.id,
            space_id=assistant.space_id,
            name=assistant.name,
            prompt=prompt,
            attachments=attachments,
            allowed_attachments=allowed_attachments,
            user=assistant.user,
            groups=groups,
            websites=assistant.websites,
            completion_model=assistant.completion_model,
            completion_model_kwargs=assistant.completion_model_kwargs,
            logging_enabled=assistant.logging_enabled,
            published=assistant.published,
            tools=tools,
            permissions=permissions,
        )

    def from_assistant_to_default_assistant_model(
        self,
        assistant: Assistant,
        permissions: list["ResourcePermission"],
    ):
        assistant_public = self.from_assistant_to_model(
            assistant=assistant, permissions=permissions
        )

        return DefaultAssistant(
            **assistant_public.model_dump(),
        )
