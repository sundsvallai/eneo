from instorage.assistants.api.assistant_models import AssistantPublic
from instorage.assistants.assistant import Assistant
from instorage.users.user import UserInDB


class AssistantAssembler:
    def __init__(self, user: UserInDB):
        self.user = user

    def from_assistant_to_model(self, assistant: Assistant):
        return AssistantPublic(
            created_at=assistant.created_at,
            updated_at=assistant.updated_at,
            id=assistant.id,
            space_id=assistant.space_id,
            name=assistant.name,
            prompt=assistant.prompt,
            user=assistant.user,
            groups=assistant.groups,
            websites=assistant.websites,
            completion_model=assistant.completion_model,
            completion_model_kwargs=assistant.completion_model_kwargs,
            logging_enabled=assistant.logging_enabled,
        )
