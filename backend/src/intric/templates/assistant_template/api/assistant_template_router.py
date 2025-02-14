from uuid import UUID

from fastapi import APIRouter, Depends

from intric.main.config import SETTINGS
from intric.main.container.container import Container
from intric.server.dependencies.container import get_container
from intric.server.protocol import responses
from intric.templates.assistant_template.api.assistant_template_models import (
    AssistantTemplateCreate,
    AssistantTemplateListPublic,
    AssistantTemplatePublic,
    AssistantTemplateUpdate,
)

router = APIRouter()


@router.get(
    "/",
    response_model=AssistantTemplateListPublic,
    status_code=200,
    responses=responses.get_responses([400, 404]),
)
async def get_templates(container: Container = Depends(get_container(with_user=True))):
    """Get all assistant templates"""
    service = container.assistant_template_service()
    assembler = container.assistant_template_assembler()

    templates = await service.get_assistant_templates()

    return assembler.to_paginated_response(templates)


if SETTINGS.using_intric_proprietary:
    from intric_prop.authentication import auth

    @router.get(
        "/admin/",
        response_model=AssistantTemplateListPublic,
        status_code=200,
        responses=responses.get_responses([400, 404]),
        dependencies=[Depends(auth.authenticate_super_api_key)],
    )
    async def get_templates_admin(container: Container = Depends(get_container())):
        """Get all assistant templates from Admin"""
        service = container.assistant_template_service()
        assembler = container.assistant_template_assembler()

        templates = await service.get_assistant_templates()

        return assembler.to_paginated_response(templates)

    @router.get(
        "/{id}/",
        response_model=AssistantTemplatePublic,
        status_code=200,
        responses=responses.get_responses([400, 404]),
    )
    async def get_assistant_template(
        id: UUID,
        container: Container = Depends(get_container(with_user=True)),
    ):
        service = container.assistant_template_service()
        assembler = container.assistant_template_assembler()

        assistant_template = await service.get_assistant_template(
            assistant_template_id=id
        )

        return assembler.from_domain_to_model(assistant_template)

    @router.post(
        "/",
        status_code=201,
        responses=responses.get_responses([400, 404]),
        dependencies=[Depends(auth.authenticate_super_api_key)],
    )
    async def create_assistant_template(
        template_create: AssistantTemplateCreate,
        container: Container = Depends(get_container()),
    ):
        service = container.assistant_template_service()

        await service.create_assistant_template(obj=template_create)

    @router.delete(
        "/{id}/",
        status_code=204,
        responses=responses.get_responses([400, 404]),
        dependencies=[Depends(auth.authenticate_super_api_key)],
    )
    async def delete_assistant_template(
        id: UUID,
        container: Container = Depends(get_container()),
    ):
        service = container.assistant_template_service()
        await service.delete_assistant_template(id=id)

    @router.put(
        "/{id}/",
        status_code=200,
        responses=responses.get_responses([400, 404]),
        dependencies=[Depends(auth.authenticate_super_api_key)],
    )
    async def update_assistant_template(
        id: UUID,
        template_update: AssistantTemplateUpdate,
        container: Container = Depends(get_container()),
    ):
        service = container.assistant_template_service()
        assembler = container.assistant_template_assembler()
        template = await service.update_assistant_template(id=id, obj=template_update)

        return assembler.from_domain_to_model(assistant_template=template)
