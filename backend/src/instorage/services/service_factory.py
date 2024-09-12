from dependency_injector import providers
from fastapi import Depends, Path

from instorage.groups.group import GroupInDB
from instorage.main.container.container import Container
from instorage.main.container.container_overrides import (
    override_completion_model,
    override_embedding_model,
)
from instorage.server.dependencies.container import get_container
from instorage.services.output_parsing.output_parser_factory import OutputParserFactory
from instorage.services.service import Service


def get_services_service(container: Container = Depends(get_container(with_user=True))):
    return container.service_service()


async def get_runner_from_service(
    id: str = Path(), container: Container = Depends(get_container(with_user=True))
):
    service = await container.service_service().get_service(id)

    override_completion_model(
        container=container, completion_model=service.completion_model
    )

    if service.groups:
        embedding_model = await container.ai_models_service().get_embedding_model(
            service.groups[0].embedding_model_id
        )
        override_embedding_model(container=container, embedding_model=embedding_model)
    else:
        container.datastore.override(providers.Object(None))

    return get_service_runner(container=container, service=service)


def get_service_runner(
    container: Container,
    service: Service,
    with_groups: list[GroupInDB] = None,
):
    if with_groups is not None:
        service.groups = with_groups

    output_parser = OutputParserFactory.create(service)
    prompt = f"{service.prompt}\n{output_parser.get_format_instructions()}"

    return container.service_runner(
        service=service, output_parser=output_parser, prompt=prompt
    )
