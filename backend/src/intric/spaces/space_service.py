from typing import TYPE_CHECKING
from uuid import UUID

from intric.ai_models.ai_models_service import AIModelsService
from intric.ai_models.completion_models.completion_model import CompletionModelPublic
from intric.ai_models.embedding_models.embedding_model import EmbeddingModelPublic
from intric.main.exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
)
from intric.spaces.api.space_models import SpaceMember, SpaceRoleValue
from intric.spaces.space import Space
from intric.spaces.space_factory import SpaceFactory
from intric.spaces.space_repo import SpaceRepository
from intric.users.user import UserInDB
from intric.users.user_repo import UsersRepository

if TYPE_CHECKING:
    from intric.actors import ActorManager
    from intric.completion_models.application import CompletionModelCRUDService


class SpaceService:
    def __init__(
        self,
        user: UserInDB,
        factory: SpaceFactory,
        repo: SpaceRepository,
        user_repo: UsersRepository,
        ai_models_service: AIModelsService,
        completion_model_crud_service: "CompletionModelCRUDService",
        actor_manager: "ActorManager",
    ):
        self.user = user
        self.factory = factory
        self.repo = repo
        self.user_repo = user_repo
        self.ai_models_service = ai_models_service
        self.completion_model_crud_service = completion_model_crud_service
        self.actor_manager = actor_manager

    def _get_actor(self, space: Space):
        return self.actor_manager.get_space_actor_from_space(space)

    async def _add_models_to_personal_space(self, personal_space: Space):
        def _available_models(
            models: list[CompletionModelPublic | EmbeddingModelPublic],
        ):
            return [model for model in models if model.can_access]

        available_completion_models = (
            await self.completion_model_crud_service.get_available_completion_models()
        )
        available_embedding_models = _available_models(
            await self.ai_models_service.get_embedding_models()
        )

        personal_space.completion_models = available_completion_models
        personal_space.embedding_models = available_embedding_models

        return personal_space

    async def create_space(self, name: str):
        space = self.factory.create_space(name=name)

        def _get_latest_model(models):
            for model in sorted(
                models, key=lambda model: model.created_at, reverse=True
            ):
                if model.can_access:
                    return model

        # Set embedding models as only the latest one
        embedding_models = await self.ai_models_service.get_embedding_models()
        latest_model = _get_latest_model(embedding_models)
        space.embedding_models = [latest_model] if latest_model else []

        # Set completion models
        completion_models = (
            await self.completion_model_crud_service.get_available_completion_models()
        )
        space.completion_models = completion_models

        # Set tenant
        space.tenant_id = self.user.tenant_id

        # Set admin
        admin = SpaceMember(
            id=self.user.id,
            username=self.user.username,
            email=self.user.email,
            role=SpaceRoleValue.ADMIN,
        )
        space.add_member(admin)

        return await self.repo.add(space)

    async def get_space(self, id: UUID) -> Space:
        space = await self.repo.one(id)

        actor = self._get_actor(space)
        if not actor.can_read_space():
            raise UnauthorizedException()

        if space.is_personal():
            space = await self._add_models_to_personal_space(space)

        return space

    async def update_space(
        self,
        id: UUID,
        name: str = None,
        description: str = None,
        embedding_model_ids: list[UUID] = None,
        completion_model_ids: list[UUID] = None,
    ) -> Space:
        space = await self.get_space(id)
        actor = self._get_actor(space)

        if not actor.can_edit_space():
            raise UnauthorizedException("User does not have permission to edit space")

        completion_models = None
        if completion_model_ids is not None:
            completion_models = [
                await self.completion_model_crud_service.get_completion_model(
                    model_id=model_id
                )
                for model_id in completion_model_ids
            ]

        embedding_models = None
        if embedding_model_ids is not None:
            embedding_models = await self.ai_models_service.get_embedding_models(
                id_list=embedding_model_ids
            )

        space.update(
            name=name,
            description=description,
            completion_models=completion_models,
            embedding_models=embedding_models,
        )

        return await self.repo.update(space)

    async def delete_personal_space(self, user: UserInDB):
        space = await self.repo.get_personal_space(user.id)

        if space is not None:
            await self.repo.delete(space.id)

    async def delete_space(self, id: UUID):
        space = await self.get_space(id)
        actor = self._get_actor(space)

        if not actor.can_delete_space():
            raise UnauthorizedException("User does not have permission to delete space")

        await self.repo.delete(space.id)

    async def get_spaces(self, *, include_personal: bool = False) -> list[Space]:
        spaces = await self.repo.get_spaces_for_member(self.user.id)

        if include_personal:
            personal_space = await self.get_personal_space()
            return [personal_space] + spaces

        return spaces

    async def add_member(self, id: UUID, member_id: UUID, role: SpaceRoleValue):
        space = await self.get_space(id)
        actor = self._get_actor(space)

        if not actor.can_edit_space():
            raise UnauthorizedException("Only Admins of the space can add members")

        user = await self.user_repo.get_user_by_id_and_tenant_id(
            id=member_id, tenant_id=self.user.tenant_id
        )

        if user is None:
            raise NotFoundException("User not found")

        member = SpaceMember(
            id=member_id,
            username=user.username,
            email=user.email,
            role=role,
        )

        space.add_member(member)
        space = await self.repo.update(space)

        return space.get_member(member.id)

    async def remove_member(self, id: UUID, user_id: UUID):
        if user_id == self.user.id:
            raise BadRequestException("Can not remove yourself")

        space = await self.get_space(id)
        actor = self._get_actor(space)

        if not actor.can_edit_space():
            raise UnauthorizedException("Only Admins of the space can remove members")

        space.remove_member(user_id)

        await self.repo.update(space)

    async def change_role_of_member(
        self, id: UUID, user_id: UUID, new_role: SpaceRoleValue
    ):
        if user_id == self.user.id:
            raise BadRequestException("Can not change role of yourself")

        space = await self.get_space(id)
        actor = self._get_actor(space)

        if not actor.can_edit_space():
            raise UnauthorizedException(
                "Only Admins of the space can change the roles of members"
            )

        space.change_member_role(user_id, new_role)
        space = await self.repo.update(space)

        return space.get_member(user_id)

    async def create_personal_space(self):
        space_name = f"{self.user.username}'s personal space"
        space = self.factory.create_space(name=space_name, user_id=self.user.id)

        # Set tenant
        space.tenant_id = self.user.tenant_id

        space_in_db = await self.repo.add(space)

        return await self._add_models_to_personal_space(space_in_db)

    async def get_personal_space(self):
        personal_space = await self.repo.get_personal_space(self.user.id)

        if personal_space is None:
            return

        return await self._add_models_to_personal_space(personal_space)
