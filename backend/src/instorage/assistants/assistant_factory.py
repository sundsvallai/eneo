from uuid import UUID

from instorage.ai_models.completion_models.completion_model import (
    CompletionModelPublic,
    ModelKwargs,
)
from instorage.assistants.assistant import Assistant
from instorage.database.tables.assistant_table import Assistants
from instorage.database.tables.groups_table import Groups
from instorage.groups.group import GroupMetadata, GroupSparse
from instorage.main.logging import get_logger
from instorage.main.models import IdAndName
from instorage.users.user import UserInDB, UserSparse
from instorage.websites.website_models import WebsiteSparse

logger = get_logger(__name__)


class AssistantFactory:
    @staticmethod
    def create_assistant(
        name: str,
        prompt: str | None,
        user: UserInDB,
        space_id: UUID | None,
        completion_model_kwargs: ModelKwargs = ModelKwargs(),
        logging_enabled: bool = False,
    ) -> Assistant:
        return Assistant(
            id=None,
            user=user,
            space_id=space_id,
            name=name,
            prompt=prompt,
            completion_model=None,
            completion_model_kwargs=completion_model_kwargs,
            logging_enabled=logging_enabled,
            websites=[],
            groups=[],
        )

    @staticmethod
    def create_assistant_from_db(
        assistant_in_db: Assistants, groups_in_db: list[tuple[Groups, int]] = []
    ) -> Assistant:
        completion_model = None
        if assistant_in_db.completion_model_id is not None:
            completion_model = CompletionModelPublic.model_validate(
                assistant_in_db.completion_model
            )

        groups = [
            GroupSparse(
                **group.to_dict(),
                metadata=GroupMetadata(num_info_blobs=info_blob_count),
                embedding_model=IdAndName.model_validate(group.embedding_model)
            )
            for group, info_blob_count in groups_in_db
        ]
        websites = [
            WebsiteSparse.model_validate(website)
            for website in assistant_in_db.websites
        ]
        user = UserSparse.model_validate(assistant_in_db.user)
        completion_model_kwargs = ModelKwargs.model_validate(
            assistant_in_db.completion_model_kwargs
        )

        return Assistant(
            id=assistant_in_db.id,
            user=user,
            space_id=assistant_in_db.space_id,
            name=assistant_in_db.name,
            prompt=assistant_in_db.prompt,
            completion_model=completion_model,
            completion_model_kwargs=completion_model_kwargs,
            logging_enabled=assistant_in_db.logging_enabled,
            websites=websites,
            groups=groups,
            created_at=assistant_in_db.created_at,
            updated_at=assistant_in_db.updated_at,
        )
