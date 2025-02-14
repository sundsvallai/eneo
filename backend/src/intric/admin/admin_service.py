from intric.admin.admin_models import PrivacyPolicy
from intric.main.exceptions import BadRequestException, NotFoundException
from intric.roles.permissions import Permission, validate_permissions
from intric.tenants.tenant_repo import TenantRepository
from intric.users.user import (
    UserAddAdmin,
    UserAddSuperAdmin,
    UserInDB,
    UserUpdatePublic,
)
from intric.users.user_repo import UsersRepository
from intric.users.user_service import UserService


class AdminService:
    def __init__(
        self,
        user: UserInDB,
        user_repo: UsersRepository,
        tenant_repo: TenantRepository,
        user_service: UserService,
    ):
        self.user = user
        self.user_repo = user_repo
        self.tenant_repo = tenant_repo
        self.user_service = user_service

    @validate_permissions(Permission.ADMIN)
    async def get_tenant_users(self):
        return await self.user_repo.get_all_users(self.user.tenant_id)

    @validate_permissions(Permission.ADMIN)
    async def register_tenant_user(self, user: UserAddAdmin):
        user_with_tenant = UserAddSuperAdmin(
            **user.model_dump(), tenant_id=self.user.tenant_id
        )

        return await self.user_service.register(user_with_tenant)

    @validate_permissions(Permission.ADMIN)
    async def update_tenant_user(self, username: str, user: UserUpdatePublic):
        user_in_db = await self.user_repo.get_user_by_username(username)

        if user_in_db is None or user_in_db.tenant_id != self.user.tenant_id:
            raise NotFoundException()

        return await self.user_service.update_user(user_in_db.id, user)

    @validate_permissions(Permission.ADMIN)
    async def delete_tenant_user(self, username: str):
        user_in_db = await self.user_repo.get_user_by_username(username)

        if user_in_db is None or user_in_db.tenant_id != self.user.tenant_id:
            raise NotFoundException()

        if user_in_db.id == self.user.id:
            raise BadRequestException("You can not delete yourself.")

        return await self.user_service.delete_user(user_in_db.id)

    @validate_permissions(Permission.ADMIN)
    async def update_privacy_policy(self, privacy_policy: PrivacyPolicy):
        return await self.tenant_repo.set_privacy_policy(
            privacy_policy.url, tenant_id=self.user.tenant_id
        )
