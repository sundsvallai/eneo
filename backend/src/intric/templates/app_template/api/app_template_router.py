from uuid import UUID

from fastapi import APIRouter, Depends

from intric.main.config import SETTINGS
from intric.main.container.container import Container
from intric.server.dependencies.container import get_container
from intric.server.protocol import responses
from intric.templates.app_template.api.app_template_models import (
    AppTemplateCreate,
    AppTemplateListPublic,
    AppTemplatePublic,
    AppTemplateUpdate,
)

router = APIRouter()


@router.get(
    "/",
    response_model=AppTemplateListPublic,
    status_code=200,
    responses=responses.get_responses([400, 404]),
)
async def get_templates(
    container: Container = Depends(get_container(with_user=True)),
):
    """Get all app templates"""
    service = container.app_template_service()
    assembler = container.app_template_assembler()

    app_templates = await service.get_app_templates()

    return assembler.to_paginated_response(items=app_templates)


if SETTINGS.using_intric_proprietary:
    from intric_prop.authentication import auth

    @router.get(
        "/admin/",
        response_model=AppTemplateListPublic,
        status_code=200,
        responses=responses.get_responses([400, 404]),
        dependencies=[Depends(auth.authenticate_super_api_key)],
    )
    async def get_templates_admin(
        container: Container = Depends(get_container()),
    ):
        """Get all app templates from Admin"""
        service = container.app_template_service()
        assembler = container.app_template_assembler()

        app_templates = await service.get_app_templates()

        return assembler.to_paginated_response(items=app_templates)

    @router.get(
        "/{id}",
        response_model=AppTemplatePublic,
        status_code=200,
        responses=responses.get_responses([400, 404]),
    )
    async def get_app_template(
        id: UUID,
        container: Container = Depends(get_container(with_user=True)),
    ):
        service = container.app_template_service()
        assembler = container.app_template_assembler()

        app_template = await service.get_app_template(app_template_id=id)

        return assembler.from_domain_to_model(app_template=app_template)

    @router.post(
        "/",
        status_code=201,
        responses=responses.get_responses([400, 404]),
        dependencies=[Depends(auth.authenticate_super_api_key)],
    )
    async def create_app_template(
        template_create: AppTemplateCreate,
        container: Container = Depends(get_container()),
    ):
        service = container.app_template_service()

        await service.create_app_template(obj=template_create)

    @router.delete(
        "/{id}/",
        status_code=204,
        responses=responses.get_responses([400, 404]),
        dependencies=[Depends(auth.authenticate_super_api_key)],
    )
    async def delete_app_template(
        id: UUID,
        container: Container = Depends(get_container()),
    ):
        service = container.app_template_service()
        await service.delete_app_template(id=id)

    @router.put(
        "/{id}/",
        response_model=AppTemplatePublic,
        status_code=200,
        responses=responses.get_responses([400, 404]),
        dependencies=[Depends(auth.authenticate_super_api_key)],
    )
    async def update_app_template(
        id: UUID,
        template_update: AppTemplateUpdate,
        container: Container = Depends(get_container()),
    ):
        service = container.app_template_service()
        assembler = container.app_template_assembler()
        template = await service.update_app_template(id=id, obj=template_update)

        return assembler.from_domain_to_model(app_template=template)
