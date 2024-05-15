from uuid import UUID

from instorage.ai_models.completion_models.llms import (
    ModelHostingLocation,
    get_completion_model,
)
from instorage.assistants.assistant import (
    AssistantBase,
    AssistantCreatePublic,
    AssistantGuard,
    AssistantInDBWithUser,
    AssistantUpdatePublic,
    AssistantUpsert,
)
from instorage.assistants.assistant_repo import AssistantRepository
from instorage.authentication.auth_service import AuthService
from instorage.main.exceptions import (
    AuthenticationException,
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
)
from instorage.modules.module import Modules
from instorage.roles.permissions import (
    Permission,
    validate_permission,
    validate_permissions,
)
from instorage.services.service import ServiceBase, ServiceInDBWithUser, ServiceUpsert
from instorage.services.service_repo import ServiceRepository
from instorage.users.user import UserInDB
from instorage.workflows.step_repo import StepRepository
from instorage.workflows.workflow import Filter, FilterType, Step


class AgentServiceDelegate:
    def __init__(
        self,
        repo: AssistantRepository | ServiceRepository,
        user: UserInDB,
    ):
        self.repo = repo
        self.user = user

    def check_permissions(self, agent: AssistantInDBWithUser | ServiceInDBWithUser):
        if self.user.id != agent.user_id:
            if not agent.user_groups_ids.intersection(self.user.user_groups_ids):
                raise AuthenticationException(
                    f"User is not an owner of assistant/service({agent.uuid}) "
                    "or part of the same user group"
                )

    def set_can_edit(self, agent: AssistantInDBWithUser | ServiceInDBWithUser):
        agent.can_edit = (
            self.user.id == agent.user.id or Permission.EDITOR in self.user.permissions
        )

        return agent

    def validate(self, assistant: AssistantBase | ServiceBase):
        if assistant.logging_enabled:
            validate_permission(self.user, Permission.COMPLIANCE)

        if assistant.is_public:
            validate_permission(self.user, Permission.DEPLOYER)

        if assistant.completion_model is not None:
            model = get_completion_model(assistant.completion_model)

            if not model.selectable:
                raise BadRequestException(
                    f"CompletionModel {model.name} not supported anymore."
                )

            if (
                model.hosting == ModelHostingLocation.EU
                and Modules.EU_HOSTING not in self.user.modules
            ):
                raise UnauthorizedException(
                    "Unauthorized. Please upgrade to eu_hosting in order to access."
                )

    def validate_groups(self, agent: AssistantInDBWithUser | ServiceInDBWithUser):
        if agent.groups is None:
            return

        for group in agent.groups:
            if group.tenant_id != self.user.tenant_id or (
                group.user_id != self.user.id and not group.is_public
            ):
                raise NotFoundException(f"Group {group.id} not found")

        if len(set(group.embedding_model for group in agent.groups)) > 1:
            raise BadRequestException("All groups must have the same embedding model")

        if len(set(group.index_type for group in agent.groups)) > 1:
            raise BadRequestException("All groups must have the same index type")

    def raise_not_found_if_not_found(self, assistant):
        if assistant is None:
            raise NotFoundException()

    async def get_agent(self, uuid: UUID):
        agent = await self.repo.get_by_uuid(uuid)

        self.raise_not_found_if_not_found(agent)

        return agent

    async def delete_agent(self, uuid: UUID):
        assistant = await self.repo.delete(uuid, self.user.id)

        self.raise_not_found_if_not_found(assistant)

        return assistant


class AssistantService:
    def __init__(
        self,
        repo: AssistantRepository,
        user: UserInDB,
        auth_service: AuthService,
        service_repo: ServiceRepository,
        step_repo: StepRepository,
    ):
        self.repo = repo
        self.user = user
        self.auth_service = auth_service
        self.service_repo = service_repo
        self.step_repo = step_repo

        self.delegate = AgentServiceDelegate(repo=repo, user=user)

    def _validate(self, assistant: AssistantCreatePublic | AssistantUpdatePublic):
        self.delegate.validate(assistant)

    def _set_can_edit(self, assistant: AssistantInDBWithUser):
        if Permission.ASSISTANTS not in self.user.permissions:
            assistant.can_edit = False
            return assistant

        return self.delegate.set_can_edit(assistant)

    @validate_permissions(Permission.ASSISTANTS)
    async def create_assistant(self, assistant: AssistantCreatePublic):
        self.delegate.validate(assistant)

        assistant_upsert = AssistantUpsert(
            **assistant.model_dump(), user_id=self.user.id
        )

        if assistant.guardrail is not None:
            assistant_upsert.guardrail_active = assistant.guardrail.guardrail_active

        assistant_in_db = await self.repo.add(assistant_upsert)

        self.delegate.validate_groups(assistant_in_db)

        if assistant.guardrail is not None:
            guard_step = await self.create_guardrailstep(
                assistant_in_db, assistant.guardrail
            )
        else:
            guard_step = None

        assistant_in_db = self._set_can_edit(assistant_in_db)
        return assistant_in_db, guard_step

    @validate_permissions(Permission.ASSISTANTS)
    async def update_assistant(self, assistant: AssistantUpdatePublic, uuid: UUID):
        self.delegate.validate(assistant)

        assistant_upsert = AssistantUpsert(
            **assistant.model_dump(exclude_unset=True),
            user_id=self.user.id,
            uuid=uuid,
        )

        if assistant.guardrail is not None:
            if assistant.guardrail.guardrail_active is not None:
                assistant_upsert.guardrail_active = assistant.guardrail.guardrail_active

        assistant_in_db = await self.repo.update(assistant_upsert)

        self.delegate.raise_not_found_if_not_found(assistant_in_db)
        self.delegate.validate_groups(assistant_in_db)

        # Create/Update guardrail
        if assistant.guardrail is not None:
            if assistant_in_db.guard_step is not None:
                guard_step = await self.update_guardrailstep(
                    assistant_in_db, assistant.guardrail
                )
            else:
                guard_step = await self.create_guardrailstep(
                    assistant_in_db, assistant.guardrail
                )
        else:
            guard_step = None

        assistant_in_db = self._set_can_edit(assistant_in_db)
        return assistant_in_db, guard_step

    async def get_assistant(self, uuid: UUID) -> AssistantInDBWithUser:
        assistant = await self.delegate.get_agent(uuid)

        self.delegate.check_permissions(assistant)
        assistant = self._set_can_edit(assistant)
        return assistant

    async def get_assistants(self, name: str = None, for_tenant: bool = False):
        if for_tenant:
            return await self.get_tenant_assistants(name)

        assistants = await self.repo.get_for_user(self.user.id, search_query=name)

        for assistant in assistants:
            assistant = self._set_can_edit(assistant)

        return assistants

    async def get_public_assistants(self, name: str = None):
        assistants = await self.repo.get_public(self.user.tenant_id, search_query=name)

        for assistant in assistants:
            assistant = self._set_can_edit(assistant)

        return assistants

    @validate_permissions(Permission.ADMIN)
    async def get_tenant_assistants(self, name: str = None):
        assistants = await self.repo.get_for_tenant(
            tenant_id=self.user.tenant_id, search_query=name
        )
        for assistant in assistants:
            assistant = self._set_can_edit(assistant)

        return assistants

    @validate_permissions(Permission.ASSISTANTS)
    async def delete_assistant(self, uuid: UUID):
        return await self.delegate.delete_agent(uuid)

    @validate_permissions(Permission.DEPLOYER)
    async def generate_api_key(self, assistant_uuid: UUID):
        assistant = await self.get_assistant(assistant_uuid)

        return await self.auth_service.create_assistant_api_key(
            "ina", assistant_id=assistant.id
        )

    async def create_guardrailstep(
        self, assistant: AssistantInDBWithUser, guard: AssistantGuard
    ):
        guard_service = ServiceUpsert(
            name=f"_intric_{assistant.name}_guard_service",
            prompt=guard.guardrail_string,
            completion_model=assistant.completion_model,
            output_format="boolean",
            user_id=self.user.id,
        )

        service_in_db = await self.service_repo.add(guard_service)

        guard_step = Step(
            agent_id=service_in_db.id,
            filter=Filter(
                type=FilterType.BOOLEAN, chain_breaker_message=guard.on_fail_message
            ),
        )

        step = await self.step_repo.add(guard_step)
        await self.repo.add_guard(guard_step_id=step.id, assistant_id=assistant.id)

        return step

    async def update_guardrailstep(
        self, assistant: AssistantInDBWithUser, guard: AssistantGuard
    ):
        service_update = ServiceUpsert(
            prompt=guard.guardrail_string,
            id=assistant.guard_step.service.id,
            uuid=assistant.guard_step.service.uuid,
            user_id=self.user.id,
        )
        await self.service_repo.update(service_update)

        await self.step_repo.update_chain_breaker_message(
            assistant.guard_step.filter.id,
            chain_breaker_message=guard.on_fail_message,
        )

        return await self.step_repo.get(assistant.guard_step.id)
