# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

from uuid import UUID

from fastapi import Depends

from instorage.analysis.analysis import AskAnalysis
from instorage.main.container.container import Container
from instorage.main.container.container_overrides import override_completion_model
from instorage.server.dependencies.container import get_container


def get_analysis_service(container: Container = Depends(get_container(with_user=True))):
    return container.analysis_service(completion_service=None)


async def get_analysis_service_with_completion_service(
    assistant_id: UUID,
    ask_analysis: AskAnalysis,
    container: Container = Depends(get_container(with_user=True)),
):
    if ask_analysis.completion_model_id is None:
        assistant = await container.assistant_service().get_assistant(assistant_id)
        completion_model_id = assistant.completion_model.id
    else:
        completion_model_id = ask_analysis.completion_model_id

    completion_model = await container.ai_models_service().get_completion_model(
        completion_model_id
    )

    override_completion_model(container=container, completion_model=completion_model)

    return container.analysis_service()
