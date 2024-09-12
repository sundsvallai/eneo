from uuid import UUID

from dependency_injector import providers
from fastapi import Depends, Path

from instorage.assistants.assistant import Assistant
from instorage.main.container.container import Container
from instorage.main.container.container_overrides import (
    override_completion_model,
    override_embedding_model,
)
from instorage.server.dependencies.container import get_container


async def get_guard_runner_from_assistant(container: Container, assistant: Assistant):
    # Set container config
    override_completion_model(
        container=container, completion_model=assistant.completion_model
    )

    if assistant.groups:
        embedding_model = await container.ai_models_service().get_embedding_model(
            assistant.groups[0].embedding_model.id
        )
        override_embedding_model(container=container, embedding_model=embedding_model)
    elif assistant.websites:
        embedding_model = await container.ai_models_service().get_embedding_model(
            assistant.websites[0].embedding_model.id
        )
        override_embedding_model(container=container, embedding_model=embedding_model)

    else:
        # Not the cleanest
        container.datastore.override(providers.Object(None))

    runner = container.assistant_runner(assistant=assistant)

    return container.assistant_guard_runner(assistant_runner=runner, guard_step=None)


async def get_assistant_guard_runner(
    id: UUID = Path(),
    container: Container = Depends(
        get_container(with_user_from_assistant_api_key=True)
    ),
):
    # Get assistant specification
    assistant = await container.assistant_service().get_assistant(id)

    return await get_guard_runner_from_assistant(
        container=container, assistant=assistant
    )
