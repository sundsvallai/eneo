# Copyright (c) 2025 Sundsvalls Kommun
#
# Licensed under the MIT License.

from uuid import UUID

from fastapi import APIRouter, Depends

from intric.main.container.container import Container
from intric.security_classifications.presentation.security_classification_models import (
    SecurityClassificationCreatePublic,
    SecurityClassificationLevelsUpdateRequest,
    SecurityClassificationPublic,
    SecurityClassificationResponse,
    SecurityClassificationSingleUpdate,
    SecurityClassificationsListPublic,
    SecurityEnableRequest,
    SecurityEnableResponse,
)
from intric.server.dependencies.container import get_container
from intric.server.protocol import responses

router = APIRouter()


@router.post(
    "/",
    response_model=SecurityClassificationPublic,
    status_code=201,
    responses=responses.get_responses([400]),
)
async def create_security_classification(
    request: SecurityClassificationCreatePublic,
    container: Container = Depends(get_container(with_user=True)),
) -> SecurityClassificationPublic:
    """Create a new security classification for the current tenant.
    Args:
        request: The security classification creation request.
    Returns:
        The created security classification.
    Raises:
        400: If the request is invalid. Names must be unique.
    """
    service = container.security_classification_service()

    security_classification = await service.create_security_classification(
        name=request.name,
        description=request.description,
        set_lowest_security=request.set_lowest_security,
    )
    return SecurityClassificationPublic.from_domain(
        security_classification, return_none_if_not_enabled=False
    )


@router.get(
    "/",
    response_model=SecurityClassificationResponse,
    responses=responses.get_responses([403]),
)
async def list_security_classifications(
    container: Container = Depends(get_container(with_user=True)),
) -> list[SecurityClassificationPublic]:
    """List all security classifications ordered by security classification level.
    Returns:
        List of security classifications ordered by security classification level.
    Raises:
        403: If the user doesn't have permission to list security classifications.
    """
    service = container.security_classification_service()

    security_classifications = await service.list_security_classifications()
    user = container.user()

    scs = [
        SecurityClassificationPublic.from_domain(sc, return_none_if_not_enabled=False)
        for sc in security_classifications
    ]

    return SecurityClassificationResponse(
        security_enabled=user.tenant.security_enabled,
        security_classifications=scs,
    )


@router.get(
    "/{id}/",
    response_model=SecurityClassificationPublic,
    responses=responses.get_responses([403, 404]),
)
async def get_security_classification(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
) -> SecurityClassificationPublic:
    """Get a security classification by ID.
    Args:
        id: The ID of the security classification.
    Returns:
        The security classification.
    Raises:
        403: If the user doesn't have permission to view the security classification.
        404: If the security classification doesn't exist or belongs to a different tenant.
    """
    service = container.security_classification_service()
    security_classification = await service.get_security_classification(id)
    return SecurityClassificationPublic.from_domain(
        security_classification, return_none_if_not_enabled=False
    )


@router.patch(
    "/",
    response_model=SecurityClassificationsListPublic,
    responses=responses.get_responses([400, 403, 404]),
)
async def update_security_classification_levels(
    request: SecurityClassificationLevelsUpdateRequest,
    container: Container = Depends(get_container(with_user=True)),
) -> SecurityClassificationPublic:
    """Update the security levels of security classifications.
    Args:
        request: Security classifications to update.
    Returns:
        The updated security classifications.
    Raises:
        400: If the request is invalid.
        403: If the user doesn't have permission to update the security classification.
        404: If the security classification doesn't exist or belongs to a different tenant.
    """
    service = container.security_classification_service()

    sc_ids = [model.id for model in request.security_classifications]
    security_classifications = await service.update_security_levels(security_classifications=sc_ids)
    return SecurityClassificationsListPublic(
        security_classifications=[
            SecurityClassificationPublic.from_domain(sc, return_none_if_not_enabled=False)
            for sc in security_classifications
        ]
    )


@router.delete(
    "/{id}/",
    status_code=204,
    responses=responses.get_responses([403, 404]),
)
async def delete_security_classification(
    id: UUID,
    container: Container = Depends(get_container(with_user=True)),
) -> None:
    """Delete a security classification.
    Args:
        id: The ID of the security classification to delete.
    Raises:
        403: If the user doesn't have permission to delete the security classification.
        404: If the security classification doesn't exist.
    """
    service = container.security_classification_service()

    await service.delete_security_classification(id)


@router.patch(
    "/{id}/",
    response_model=SecurityClassificationPublic,
    responses=responses.get_responses([400, 403, 404]),
)
async def update_security_classification(
    id: UUID,
    request: SecurityClassificationSingleUpdate,
    container: Container = Depends(get_container(with_user=True)),
) -> SecurityClassificationPublic:
    """Update a single security classification's name and/or description.

    This endpoint allows updating just the name and description of a security classification
    without changing its security level.

    Args:
        id: The ID of the security classification to update
        request: The update request containing new name and/or description

    Returns:
        The updated security classification

    Raises:
        400: If the request is invalid or security is disabled. Names must be unique.
        403: If the user doesn't have permission to update the classification
        404: If the security classification doesn't exist
    """
    service = container.security_classification_service()

    security_classification = await service.update_security_classification(
        id=id, name=request.name, description=request.description
    )

    return SecurityClassificationPublic.from_domain(
        security_classification, return_none_if_not_enabled=False
    )


@router.post(
    "/enable/",
    response_model=SecurityEnableResponse,
    responses=responses.get_responses([400, 403]),
)
async def toggle_security_classifications(
    request: SecurityEnableRequest,
    container: Container = Depends(get_container(with_user=True)),
) -> SecurityEnableResponse:
    """Enable or disable security classifications for the current tenant.

    Args:
        request: Contains a flag to enable or disable security classifications.

    Returns:
        The updated tenant information with security_enabled status.

    Raises:
        400: If the request is invalid.
        403: If the user doesn't have permission to update tenant settings.
    """
    service = container.security_classification_service()
    tenant = await service.toggle_security_on_tenant(enabled=request.enabled)

    return SecurityEnableResponse(
        tenant_id=tenant.id,
        security_enabled=tenant.security_enabled,
    )
