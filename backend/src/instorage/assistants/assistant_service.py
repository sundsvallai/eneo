from datetime import datetime
from uuid import UUID

from instorage.ai_models.ai_models_service import AIModelsService
from instorage.ai_models.completion_models.completion_model import ModelKwargs
from instorage.assistants.api.assistant_models import (
    AssistantCreate,
    AssistantGuard,
    AssistantUpdate,
)
from instorage.assistants.assistant import Assistant
from instorage.assistants.assistant_factory import AssistantFactory
from instorage.assistants.assistant_repo import AssistantRepository
from instorage.authentication.auth_service import AuthService
from instorage.groups.group_service import GroupService
from instorage.main.exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
)
from instorage.roles.permissions import (
    Permission,
    validate_permission,
    validate_permissions,
)
from instorage.services.service import ServiceCreate, ServiceUpdate
from instorage.services.service_repo import ServiceRepository
from instorage.spaces.space import SpacePermissionsActions
from instorage.spaces.space_service import SpaceService
from instorage.users.user import UserInDB
from instorage.websites.website_service import WebsiteService
from instorage.workflows.step_repo import StepRepository
from instorage.workflows.workflow import Filter, FilterType, Step


class AssistantService:
    def __init__(
        self,
        repo: AssistantRepository,
        user: UserInDB,
        auth_service: AuthService,
        service_repo: ServiceRepository,
        step_repo: StepRepository,
        ai_models_service: AIModelsService,
        group_service: GroupService,
        website_service: WebsiteService,
        space_service: SpaceService,
        factory: AssistantFactory,
    ):
        self.repo = repo
        self.factory = factory
        self.user = user
        self.auth_service = auth_service
        self.service_repo = service_repo
        self.step_repo = step_repo
        self.ai_models_service = ai_models_service
        self.website_service = website_service
        self.group_service = group_service
        self.space_service = space_service

    async def _check_space_permissions(
        self,
        assistant: Assistant,
        action: SpacePermissionsActions = SpacePermissionsActions.READ,
    ):
        space = await self.space_service.get_space(assistant.space_id)

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

                if not space.can_delete_resource(self.user, assistant.user.id):
                    raise UnauthorizedException()

    async def check_permissions(
        self,
        assistant: Assistant,
        action: SpacePermissionsActions = SpacePermissionsActions.READ,
    ):
        if assistant.space_id is not None:
            await self._check_space_permissions(assistant=assistant, action=action)

        elif self.user.id != assistant.user.id:
            raise NotFoundException()

    async def set_can_edit(self, assistant: Assistant):
        if assistant.space_id is not None:
            space = await self.space_service.get_space(assistant.space_id)
            assistant.can_edit = space.can_edit_resource(self.user)

        else:
            assistant.can_edit = (
                self.user.id == assistant.user.id
                or Permission.EDITOR in self.user.permissions
            )

        return assistant

    async def validate_space_assistant(self, assistant: Assistant):
        if assistant.space_id is None:
            return

        space = await self.space_service.get_space(assistant.space_id)

        # validate completion model
        if assistant.completion_model is not None:
            if not space.is_completion_model_in_space(assistant.completion_model.id):
                raise BadRequestException("Completion model is not in space.")

        # validate groups
        for group in assistant.groups:
            if not space.is_group_in_space(group.id):
                raise BadRequestException("Group is not in space.")

        # validate websites
        for website in assistant.websites:
            if not space.is_website_in_space(website.id):
                raise BadRequestException("Website is not in space.")

        await self._validate_same_embedding_model(assistant)

    async def _validate_same_embedding_model(
        self, assistant: AssistantCreate | AssistantUpdate
    ):
        if not assistant.websites and not assistant.groups:
            return

        embedding_model_ids = set()
        if assistant.websites:
            websites = await self.website_service.get_websites_by_ids(
                [website.id for website in assistant.websites]
            )

            for website in websites:
                if website.embedding_model_id is None:
                    raise BadRequestException(
                        f"Website({website.id}) has no embedding model set"
                    )

                embedding_model_ids.add(website.embedding_model_id)

        if assistant.groups:
            groups_in_db = await self.group_service.get_groups_by_ids(
                [group.id for group in assistant.groups]
            )

            embedding_model_ids.update(
                [group.embedding_model_id for group in groups_in_db]
            )

        if len(embedding_model_ids) > 1:
            raise BadRequestException(
                "All websites and groups must have the same embedding model"
            )

    @validate_permissions(Permission.ASSISTANTS)
    async def create_assistant(
        self,
        name: str,
        prompt: str,
        completion_model_id: UUID,
        completion_model_kwargs: ModelKwargs = ModelKwargs(),
        logging_enabled: bool = False,
        groups: list[UUID] = [],
        websites: list[UUID] = [],
    ):
        if logging_enabled:
            validate_permission(self.user, Permission.ADMIN)

        assistant = self.factory.create_assistant(
            name=name,
            prompt=prompt,
            space_id=None,
            completion_model_kwargs=completion_model_kwargs,
            logging_enabled=logging_enabled,
            user=self.user,
        )

        # completion model
        completion_model = await self.ai_models_service.get_completion_model(
            completion_model_id
        )
        assistant.completion_model = completion_model

        # groups
        if groups:
            groups = await self.group_service.get_groups_by_ids(groups)
            assistant.groups = groups

        # websites
        if websites:
            websites = await self.website_service.get_websites_by_ids(websites)
            assistant.websites = websites

        assistant = await self.repo.add(assistant)

        assistant = await self.set_can_edit(assistant)
        return assistant

    async def create_space_assistant(self, name: str, space_id: UUID):
        space = await self.space_service.get_space(space_id)

        if not space.can_create_assistants(self.user):
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
                "Can not create an assistant in a space without enabled completion models"
            )

        assistant_create = Assistant(
            id=None,
            name=name,
            prompt="",
            user=self.user,
            space_id=space_id,
            completion_model=completion_model,
            completion_model_kwargs=ModelKwargs(),
            groups=[],
            websites=[],
            logging_enabled=False,
        )

        assistant = await self.repo.add(assistant_create)
        return await self.set_can_edit(assistant)

    async def update_assistant(
        self,
        id: UUID,
        name: str | None = None,
        prompt: str | None = None,
        completion_model_id: UUID | None = None,
        completion_model_kwargs: ModelKwargs | None = None,
        logging_enabled: bool | None = None,
        groups: list[UUID] | None = None,
        websites: list[UUID] | None = None,
    ):
        if logging_enabled:
            validate_permission(self.user, Permission.ADMIN)

        assistant = await self.get_assistant(id)

        # completion model
        completion_model = None
        if completion_model_id is not None:
            completion_model = await self.ai_models_service.get_completion_model(
                completion_model_id
            )

        # groups
        if groups is not None:
            groups = await self.group_service.get_groups_by_ids(groups)

        # websites
        if websites is not None:
            websites = await self.website_service.get_websites_by_ids(websites)

        assistant.update(
            name=name,
            prompt=prompt,
            completion_model=completion_model,
            completion_model_kwargs=completion_model_kwargs,
            logging_enabled=logging_enabled,
            groups=groups,
            websites=websites,
        )
        assistant = await self.repo.update(assistant)

        await self.check_permissions(
            assistant,
            action=SpacePermissionsActions.EDIT,
        )
        await self.validate_space_assistant(assistant)

        assistant = await self.set_can_edit(assistant)
        return assistant

    async def get_assistant(self, id: UUID) -> Assistant:
        assistant = await self.repo.get_by_id(id)

        if assistant is None:
            raise NotFoundException()

        await self.check_permissions(assistant)

        assistant = await self.set_can_edit(assistant)
        return assistant

    async def get_assistants(
        self, name: str = None, for_tenant: bool = False
    ) -> list[Assistant]:
        if for_tenant:
            return await self.get_tenant_assistants(name)

        assistants = await self.repo.get_for_user(self.user.id, search_query=name)

        for assistant in assistants:
            assistant = await self.set_can_edit(assistant)

        return assistants

    @validate_permissions(Permission.ADMIN)
    async def get_tenant_assistants(
        self,
        name: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
    ):
        assistants = await self.repo.get_for_tenant(
            tenant_id=self.user.tenant_id,
            search_query=name,
            start_date=start_date,
            end_date=end_date,
        )
        return assistants

    async def delete_assistant(self, id: UUID):
        assistant = await self.get_assistant(id)
        await self.check_permissions(
            assistant=assistant, action=SpacePermissionsActions.DELETE
        )
        await self.repo.delete(id)

    @validate_permissions(Permission.ADMIN)
    async def generate_api_key(self, assistant_id: UUID):
        assistant = await self.get_assistant(assistant_id)

        return await self.auth_service.create_assistant_api_key(
            "ina", assistant_id=assistant.id
        )

    async def create_guardrailstep(self, assistant: Assistant, guard: AssistantGuard):
        guard_service = ServiceCreate(
            name=f"_intric_{assistant.name}_guard_service",
            prompt=guard.guardrail_string,
            output_format="boolean",
            user_id=assistant.user.id,
            completion_model_id=assistant.completion_model.id,
            completion_model_kwargs=assistant.completion_model_kwargs,
        )

        service_in_db = await self.service_repo.add(guard_service)

        guard_step = Step(
            service_id=service_in_db.id,
            filter=Filter(
                type=FilterType.BOOLEAN, chain_breaker_message=guard.on_fail_message
            ),
        )

        step = await self.step_repo.add(guard_step)
        await self.repo.add_guard(guard_step_id=step.id, assistant_id=assistant.id)

        return step

    async def update_guardrailstep(self, assistant: Assistant, guard: AssistantGuard):
        service_update = ServiceUpdate(
            prompt=guard.guardrail_string,
            id=assistant.guardial.service.id,
            user_id=self.user.id,
        )
        await self.service_repo.update(service_update)

        await self.step_repo.update_chain_breaker_message(
            assistant.guardial.filter.id,
            chain_breaker_message=guard.on_fail_message,
        )

        return await self.step_repo.get(assistant.guardial.id)

    async def move_assistant_to_space(
        self, assistant_id: UUID, space_id: UUID, move_resources: bool
    ):
        target_space = await self.space_service.get_space(space_id)
        assistant = await self.get_assistant(assistant_id)

        if assistant.space_id is not None:
            source_space = await self.space_service.get_space(assistant.space_id)

            if not source_space.can_delete_resource(self.user, assistant.user.id):
                raise UnauthorizedException(
                    "User does not have permission to move assistant from space"
                )

        if not target_space.can_create_assistants(self.user):
            raise UnauthorizedException(
                "User does not have permission to create assistants in the space"
            )

        if not target_space.is_completion_model_in_space(assistant.completion_model.id):
            raise BadRequestException(
                "Space does not have completion model "
                f"{assistant.completion_model.name} enabled"
            )

        await self.repo.add_assistant_to_space(
            assistant_id=assistant_id, space_id=space_id
        )

        if move_resources:
            for group in assistant.groups:
                await self.group_service.move_group_to_space(
                    group_id=group.id,
                    space_id=space_id,
                    assistant_ids=[assistant_id],
                )

            for website in assistant.websites:
                await self.website_service.move_website_to_space(
                    website_id=website.id,
                    space_id=space_id,
                    assistant_ids=[assistant_id],
                )
