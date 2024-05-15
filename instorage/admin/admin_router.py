from fastapi import APIRouter, Depends

from instorage.admin.admin_factory import get_admin_service
from instorage.admin.admin_models import PrivacyPolicy
from instorage.admin.admin_service import AdminService
from instorage.main.models import DeleteResponse, PaginatedResponse
from instorage.server import protocol
from instorage.tenants.tenant import TenantPublic
from instorage.users.user import (
    UserAddAdmin,
    UserAdminView,
    UserCreatedAdminView,
    UserUpdatePublic,
)

router = APIRouter()


@router.get("/users/", response_model=PaginatedResponse[UserAdminView])
async def get_users(
    service: AdminService = Depends(get_admin_service),
):
    users = await service.get_tenant_users()

    users_admin_view = [UserAdminView(**user.model_dump()) for user in users]

    return protocol.to_paginated_response(users_admin_view)


@router.post("/users/", response_model=UserCreatedAdminView)
async def register_user(
    new_user: UserAddAdmin,
    service: AdminService = Depends(get_admin_service),
):
    user, _, api_key = await service.register_tenant_user(new_user)

    user_admin_view = UserCreatedAdminView(
        **user.model_dump(exclude={"api_key"}), api_key=api_key
    )

    return user_admin_view


@router.post("/users/{username}/", response_model=UserAdminView)
async def update_user(
    username: str,
    user: UserUpdatePublic,
    service: AdminService = Depends(get_admin_service),
):
    """Omitted fields are not updated."""

    user_updated = await service.update_tenant_user(username, user)

    user_admin_view = UserAdminView(**user_updated.model_dump())

    return user_admin_view


@router.delete("/users/{username}", response_model=DeleteResponse)
async def delete_user(
    username: str, service: AdminService = Depends(get_admin_service)
):
    success = await service.delete_tenant_user(username)

    return DeleteResponse(success=success)


@router.post("/privacy-policy/", response_model=TenantPublic)
async def update_privacy_policy(
    url: PrivacyPolicy, service: AdminService = Depends(get_admin_service)
):
    return await service.update_privacy_policy(url)
