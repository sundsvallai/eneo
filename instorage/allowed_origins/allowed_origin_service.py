from uuid import UUID

from pydantic.networks import HttpUrl

from instorage.allowed_origins.allowed_origin_repo import AllowedOriginRepository
from instorage.main.exceptions import AuthenticationException
from instorage.roles.permissions import Permission, validate_permissions
from instorage.users.user import UserInDB


class AllowedOriginService:
    def __init__(self, user: UserInDB, repo: AllowedOriginRepository):
        self.user = user
        self.repo = repo

    @validate_permissions(Permission.ADMIN)
    async def add(self, origins: list[HttpUrl]):
        return await self.repo.add(origins, tenant_id=self.user.tenant_id)

    @validate_permissions(Permission.ADMIN)
    async def get(self):
        return await self.repo.get_all(self.user.tenant_id)

    @validate_permissions(Permission.ADMIN)
    async def delete(self, id: UUID):
        deleted_origin = await self.repo.delete(id)

        if deleted_origin.tenant_id != self.user.tenant_id:
            AuthenticationException(
                f"User {self.user.id} tried to delete the allowed origin"
                f" {deleted_origin.url} from tenant {deleted_origin.tenant_id}"
            )

        return deleted_origin
