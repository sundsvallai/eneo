from uuid import UUID

from instorage.ai_models.ai_models_service import AIModelsService
from instorage.groups.group_service import GroupService
from instorage.main.exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
)
from instorage.questions.questions_repo import QuestionRepository
from instorage.roles.permissions import Permission, validate_permissions
from instorage.services.output_parsing.pydantic_model_factory import (
    PydanticModelFactory,
)
from instorage.services.service import (
    CreateSpaceService,
    Service,
    ServiceBase,
    ServiceCreate,
    ServiceCreatePublic,
    ServiceUpdate,
    ServiceUpdatePublic,
)
from instorage.services.service_repo import ServiceRepository
from instorage.spaces.space import SpacePermissionsActions
from instorage.spaces.space_service import SpaceService
from instorage.users.user import UserInDB


class ServiceService:
    def __init__(
        self,
        repo: ServiceRepository,
        question_repo: QuestionRepository,
        group_service: GroupService,
        user: UserInDB,
        ai_models_service: AIModelsService,
        space_service: SpaceService,
    ):
        self.repo = repo
        self.question_repo = question_repo
        self.group_service = group_service
        self.user = user
        self.space_service = space_service
        self.ai_models_service = ai_models_service

    async def _check_space_permissions(
        self,
        service: Service,
        action: SpacePermissionsActions = SpacePermissionsActions.READ,
    ):
        space = await self.space_service.get_space(service.space_id)

        match action:
            case SpacePermissionsActions.READ:
                if not space.can_read_resource(self.user):
                    raise NotFoundException()

            case SpacePermissionsActions.EDIT:
                if not space.can_read_resource(self.user):
                    raise NotFoundException()

                if not space.can_edit_resource(self.user):
                    raise UnauthorizedException()

            case SpacePermissionsActions.DELETE:
                if not space.can_read_resource(self.user):
                    raise NotFoundException()

                if not space.can_delete_resource(self.user, service.user_id):
                    raise UnauthorizedException()

    async def check_permissions(
        self,
        service: Service,
        action: SpacePermissionsActions = SpacePermissionsActions.READ,
    ):
        if service.space_id is not None:
            await self._check_space_permissions(service=service, action=action)

        elif self.user.id != service.user_id:
            raise NotFoundException()

    async def _validate(self, service: ServiceBase):
        if service.json_schema is not None:
            PydanticModelFactory(service.json_schema).validate_schema()

        if service.completion_model_id is not None:
            await self.ai_models_service.get_completion_model(
                service.completion_model_id
            )

    async def set_can_edit(self, service: Service):
        if service.space_id is not None:
            space = await self.space_service.get_space(service.space_id)
            service.can_edit = space.can_edit_resource(self.user)

        else:
            service.can_edit = (
                self.user.id == service.user_id
                or Permission.EDITOR in self.user.permissions
            )

        return service

    async def _validate_same_embedding_model(
        self, service: ServiceCreate | ServiceUpdate
    ):
        if not service.groups:
            return

        embedding_model_ids = set()
        if service.groups:
            groups_in_db = await self.group_service.get_groups_by_ids(
                [group.id for group in service.groups]
            )

            embedding_model_ids.update(
                [group.embedding_model_id for group in groups_in_db]
            )

        if len(embedding_model_ids) > 1:
            raise BadRequestException("All groups must have the same embedding model")

    async def validate_space_service(self, service: Service):
        if service.space_id is None:
            return

        space = await self.space_service.get_space(service.space_id)

        # validate completion model
        if service.completion_model_id is not None:
            if not space.is_completion_model_in_space(service.completion_model_id):
                raise BadRequestException("Completion model is not in space.")

        # validate groups
        for group in service.groups:
            if not space.is_group_in_space(group.id):
                raise BadRequestException("Group is not in space.")

        await self._validate_same_embedding_model(service)

    @validate_permissions(Permission.SERVICES)
    async def create_service(self, service: ServiceCreatePublic):
        service_create = ServiceCreate(**service.model_dump(), user_id=self.user.id)

        await self._validate(service_create)
        await self._validate_same_embedding_model(service_create)

        service_in_db = await self.repo.add(service_create)

        return await self.set_can_edit(service_in_db)

    async def create_space_service(self, name: str, space_id: UUID):
        space = await self.space_service.get_space(space_id)

        if not space.can_create_services(self.user):
            raise UnauthorizedException(
                "User does not have permission to create assistants in this space"
            )

        if space.is_personal():
            completion_model = (
                await self.ai_models_service.get_latest_available_completion_model()
            )
        else:
            completion_model = space.get_latest_completion_model()

        if completion_model is None:
            raise BadRequestException(
                "Can not create an service in a space without enabled completion models"
            )

        service_create = CreateSpaceService(
            name=name,
            prompt="",
            user_id=self.user.id,
            space_id=space_id,
            completion_model_id=completion_model.id,
        )

        service = await self.repo.add(service_create)
        return await self.set_can_edit(service)

    async def update_service(self, service: ServiceUpdatePublic, id: UUID):
        service_update = ServiceUpdate(
            **service.model_dump(exclude_unset=True),
            id=id,
        )

        await self._validate(service_update)
        await self._validate_same_embedding_model(service_update)

        service_in_db = await self.repo.update(service_update)

        if service_in_db is None:
            raise NotFoundException()

        await self.check_permissions(service_in_db)
        await self.validate_space_service(service_in_db)

        return await self.set_can_edit(service_in_db)

    async def get_service(self, uuid: UUID):
        service = await self.repo.get_by_id(uuid)

        if service is None:
            raise NotFoundException()

        await self.check_permissions(service)

        return await self.set_can_edit(service)

    async def get_services(self, name: str):
        services = await self.repo.get_for_user(self.user.id, search_query=name)
        for service in services:
            service = await self.set_can_edit(service)

        return services

    async def delete_service(self, uuid: UUID):
        service = await self.get_service(uuid)
        await self.check_permissions(
            service=service, action=SpacePermissionsActions.DELETE
        )
        await self.repo.delete(uuid)

    async def get_service_runs(self, service_uuid: str):
        service = await self.get_service(service_uuid)
        runs = await self.question_repo.get_by_service(service.id)
        return service, runs

    async def move_service_to_space(
        self, service_id: UUID, space_id: UUID, move_resources: bool
    ):
        target_space = await self.space_service.get_space(space_id)
        service = await self.get_service(service_id)

        if service.space_id is not None:
            source_space = await self.space_service.get_space(service.space_id)

            if not source_space.can_delete_resource(self.user, service.user_id):
                raise UnauthorizedException(
                    "User does not have permission to move service from space"
                )

        if not target_space.can_create_services(self.user):
            raise UnauthorizedException(
                "User does not have permission to create service in the space"
            )

        if not target_space.is_completion_model_in_space(service.completion_model.id):
            raise BadRequestException(
                "Space does not have completion model "
                f"{service.completion_model.name} enabled"
            )

        await self.repo.add_service_to_space(service_id=service_id, space_id=space_id)

        if move_resources:
            for group in service.groups:
                await self.group_service.move_group_to_space(
                    group_id=group.id,
                    space_id=space_id,
                    service_ids=[service_id],
                )
