from datetime import datetime
from uuid import UUID

from instorage.ai_models.completion_models.completion_model import (
    CompletionModelPublic,
    ModelKwargs,
)
from instorage.groups.group import GroupSparse
from instorage.main.exceptions import BadRequestException, UnauthorizedException
from instorage.users.user import UserSparse
from instorage.websites.website_models import WebsiteSparse

UNAUTHORIZED_EXCEPTION_MESSAGE = "Unauthorized. User has no permissions to access."


class Assistant:
    def __init__(
        self,
        id: UUID | None,
        user: UserSparse | None,
        space_id: UUID,
        completion_model: CompletionModelPublic | None,
        name: str,
        prompt: str,
        completion_model_kwargs: ModelKwargs,
        logging_enabled: bool,
        websites: list[WebsiteSparse],
        groups: list[GroupSparse],
        created_at: datetime = None,
        updated_at: datetime = None,
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

    def _validate_embedding_model(self, items: list[GroupSparse] | list[WebsiteSparse]):
        embedding_model_id_set = set([item.embedding_model.id for item in items])
        if len(embedding_model_id_set) != 1 or (
            self.embedding_model_id is not None
            and embedding_model_id_set.pop() != self.embedding_model_id
        ):
            raise BadRequestException(
                "All websites or groups must have the same embedding model"
            )

    def _set_groups_and_websites(
        self, groups: list[GroupSparse] | None, websites: list[WebsiteSparse] | None
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
    def groups(self, groups: list[GroupSparse]):
        self._groups.clear()

        if groups:
            self._validate_embedding_model(groups)

        self._groups = groups

    def update(
        self,
        name: str | None = None,
        prompt: str | None = None,
        completion_model: CompletionModelPublic | None = None,
        completion_model_kwargs: ModelKwargs | None = None,
        logging_enabled: bool | None = None,
        groups: list[GroupSparse] | None = None,
        websites: list[WebsiteSparse] | None = None,
    ):
        if name is not None:
            self.name = name

        if prompt is not None:
            self.prompt = prompt

        if completion_model is not None:
            self.completion_model = completion_model

        if completion_model_kwargs is not None:
            self.completion_model_kwargs = completion_model_kwargs

        if logging_enabled is not None:
            self.logging_enabled = logging_enabled

        self._set_groups_and_websites(groups=groups, websites=websites)
