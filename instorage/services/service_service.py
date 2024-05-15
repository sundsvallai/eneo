from uuid import UUID

from instorage.assistants.assistant_service import AgentServiceDelegate
from instorage.groups.group_service import GroupService
from instorage.questions.questions_repo import QuestionRepository
from instorage.roles.permissions import Permission, validate_permissions
from instorage.services.output_parsing.pydantic_model_factory import (
    PydanticModelFactory,
)
from instorage.services.service import (
    ServiceBase,
    ServiceCreatePublic,
    ServiceInDBWithUser,
    ServiceUpdatePublic,
    ServiceUpsert,
)
from instorage.services.service_repo import ServiceRepository
from instorage.users.user import UserInDB


class ServiceService:
    def __init__(
        self,
        repo: ServiceRepository,
        question_repo: QuestionRepository,
        group_service: GroupService,
        user: UserInDB,
    ):
        self.repo = repo
        self.question_repo = question_repo
        self.group_repo = group_service
        self.user = user

        self.delegate = AgentServiceDelegate(repo=repo, user=user)

    def _validate(self, service: ServiceBase):
        if service.json_schema is not None:
            PydanticModelFactory(service.json_schema).validate_schema()

        self.delegate.validate(service)

    def _set_can_edit(self, service: ServiceInDBWithUser):
        if Permission.SERVICES not in self.user.permissions:
            service.can_edit = False
            return service

        return self.delegate.set_can_edit(service)

    @validate_permissions(Permission.SERVICES)
    async def create_service(self, service: ServiceCreatePublic):
        self._validate(service)
        service_upsert = ServiceUpsert(**service.model_dump(), user_id=self.user.id)

        service_in_db = await self.repo.add(service_upsert)
        self.delegate.validate_groups(service_in_db)

        service_in_db = self._set_can_edit(service_in_db)
        return service_in_db

    @validate_permissions(Permission.SERVICES)
    async def update_service(self, service: ServiceUpdatePublic, uuid: UUID):
        self._validate(service)

        service_upsert = ServiceUpsert(
            **service.model_dump(exclude_unset=True),
            user_id=self.user.id,
            uuid=uuid,
        )

        service_in_db = await self.repo.update(service_upsert)

        self.delegate.raise_not_found_if_not_found(service_in_db)
        self.delegate.validate_groups(service_in_db)

        service_in_db = self._set_can_edit(service_in_db)
        return service_in_db

    async def get_service(self, uuid: UUID):
        service = await self.delegate.get_agent(uuid)
        self.delegate.check_permissions(service)

        service = self._set_can_edit(service)
        return service

    async def get_services(self, name: str):
        services = await self.repo.get_for_user(self.user.id, search_query=name)
        for service in services:
            service = self._set_can_edit(service)

        return services

    @validate_permissions(Permission.SERVICES)
    async def delete_service(self, uuid: UUID):
        return await self.delegate.delete_agent(uuid)

    async def get_service_runs(self, service_uuid: str):
        service = await self.delegate.get_agent(service_uuid)
        runs = await self.question_repo.get_by_service(service.id)
        return service, runs
