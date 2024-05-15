from uuid import UUID

from instorage.ai_models.completion_models.llms import ModelHostingLocation
from instorage.ai_models.embedding_models.embedding_models import get_embedding_model
from instorage.groups.group import (
    CreateGroupRequest,
    GroupCreate,
    GroupInDB,
    GroupUpdate,
    GroupUpdatePublic,
)
from instorage.groups.group_repo import GroupRepository
from instorage.info_blobs.info_blob_repo import InfoBlobRepository
from instorage.main.exceptions import (
    AuthenticationException,
    NotFoundException,
    UnauthorizedException,
)
from instorage.modules.module import Modules
from instorage.roles.permissions import (
    Permission,
    validate_permission,
    validate_permissions,
)
from instorage.tenants.tenant_repo import TenantRepository
from instorage.users.user import UserInDB


class GroupService:
    def __init__(
        self,
        user: UserInDB,
        repo: GroupRepository,
        tenant_repo: TenantRepository,
        info_blob_repo: InfoBlobRepository,
    ):
        self.user = user
        self.repo = repo
        self.tenant_repo = tenant_repo
        self.info_blob_repo = info_blob_repo

    def _set_can_edit(self, group: GroupInDB):
        if Permission.COLLECTIONS not in self.user.permissions:
            group.can_edit = False
            return group

        group.can_edit = (
            self.user.id == group.user.id or Permission.EDITOR in self.user.permissions
        )

        return group

    def _validate(self, group: GroupInDB, id: UUID):
        if group is None or group.user_id != self.user.id:
            raise NotFoundException(f"Group {id} not found")

    def _validate_permissions(self, group: GroupInDB, id: int | UUID):
        if group is None:
            raise NotFoundException(f"Group {id} not found")

        if self.user.id != group.user_id:
            if not group.user_groups_ids.intersection(self.user.user_groups_ids):
                raise AuthenticationException(
                    f"User is not an owner of group({group.uuid}) or part of the same user group"
                )

    def _validate_embedding_model(self, group: CreateGroupRequest | GroupUpdatePublic):
        if group.embedding_model is not None:
            model = get_embedding_model(group.embedding_model)
            if (
                model.hosting == ModelHostingLocation.EU
                and Modules.EU_HOSTING not in self.user.modules
            ):
                raise UnauthorizedException(
                    "Unauthorized. Please upgrade to eu_hosting in order to access."
                )

    @validate_permissions(Permission.COLLECTIONS)
    async def create_group(self, group: CreateGroupRequest):
        if group.is_public:
            validate_permission(self.user, Permission.DEPLOYER)

        self._validate_embedding_model(group)

        if group.embedding_model is None:
            group.embedding_model = self.user.tenant.default_embedding_model

        group_create = GroupCreate(
            **group.model_dump(), user_id=self.user.id, tenant_id=self.user.tenant_id
        )

        group = await self.repo.create_group(group_create)
        group = self._set_can_edit(group)
        return group

    async def get_user_groups(self):
        groups = await self.repo.get_all_groups_from_user_group(self.user.id)

        for group in groups:
            group = self._set_can_edit(group)

        return groups

    async def get_public_groups(self):
        groups = await self.repo.get_public_groups(self.user.tenant_id)

        for group in groups:
            group = self._set_can_edit(group)

        return groups

    async def get_group_by_id(self, id: int) -> GroupInDB:
        group = await self.repo.get_group_by_id(id)

        self._validate_permissions(group, id)

        group = self._set_can_edit(group)

        return group

    async def get_group_by_uuid(self, uuid: UUID) -> GroupInDB:
        group = await self.repo.get_group_by_uuid(uuid)

        self._validate_permissions(group, uuid)

        group = self._set_can_edit(group)

        return group

    @validate_permissions(Permission.COLLECTIONS)
    async def update_group(self, group_update: GroupUpdatePublic, uuid: UUID):
        if group_update.is_public:
            validate_permission(self.user, Permission.DEPLOYER)

        group = await self.get_group_by_uuid(uuid)
        self._validate(group, uuid)

        group_update = GroupUpdate(
            **group_update.model_dump(exclude_unset=True), id=group.id
        )
        group = await self.repo.update_group(group_update)

        group = self._set_can_edit(group)

        return group

    @validate_permissions(Permission.COLLECTIONS)
    async def delete_group(self, group_uuid: UUID):
        group = await self.get_group_by_uuid(group_uuid)

        self._validate(group, group.id)

        count = await self.get_count_for_group(group)

        group_deleted = await self.repo.delete_group_by_id(group.id)

        return group_deleted, True, count

    async def get_count_for_group(self, group: GroupInDB):
        return await self.info_blob_repo.get_count_of_group(group.id)

    async def get_counts_for_groups(self, groups: list[GroupInDB]):
        return [await self.get_count_for_group(group) for group in groups]
