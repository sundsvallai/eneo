from typing import TYPE_CHECKING, Optional
from uuid import UUID

from intric.ai_models.ai_models_service import AIModelsService
from intric.jobs.task_service import TaskService
from intric.main.exceptions import (
    AuthenticationException,
    BadRequestException,
    CrawlAlreadyRunningException,
    NotFoundException,
    UnauthorizedException,
)
from intric.main.models import Status
from intric.roles.permissions import (
    Permission,
    validate_permission,
    validate_permissions,
)
from intric.spaces.space_service import SpaceService
from intric.users.user import UserInDB
from intric.websites.crawl_dependencies.crawl_models import (
    CrawlRun,
    CrawlRunCreate,
    CrawlRunUpdate,
    CrawlType,
)
from intric.websites.crawl_dependencies.crawl_runs_repo import CrawlRunRepository
from intric.websites.website_models import (
    UpdateInterval,
    Website,
    WebsiteCreate,
    WebsiteCreateRequest,
    WebsiteUpdate,
    WebsiteUpdateRequest,
)
from intric.websites.website_repo import WebsiteRepository

if TYPE_CHECKING:
    from intric.actors import ActorManager


class WebsiteService:
    def __init__(
        self,
        user: UserInDB,
        repo: WebsiteRepository,
        crawl_run_repo: CrawlRunRepository,
        task_service: TaskService,
        ai_models_service: AIModelsService,
        space_service: SpaceService,
        actor_manager: "ActorManager",
    ):
        self.user = user
        self.repo = repo
        self.crawl_run_repo = crawl_run_repo
        self.task_service = task_service
        self.ai_models_service = ai_models_service
        self.space_service = space_service
        self.actor_manager = actor_manager

    def _validate(self, entity: Website | CrawlRun | None):
        if entity is None:
            raise NotFoundException()

        if entity.tenant_id != self.user.tenant_id:
            raise AuthenticationException()

    async def _crawl_website(self, website: Website):
        crawl_run = await self.crawl_run_repo.add(
            CrawlRunCreate(website_id=website.id, tenant_id=self.user.tenant_id)
        )

        crawl_job = await self.task_service.queue_crawl(
            name=website.name,
            run_id=crawl_run.id,
            website_id=website.id,
            url=website.url,
            download_files=website.download_files,
            crawl_type=website.crawl_type,
        )

        return await self.crawl_run_repo.update(
            CrawlRunUpdate(id=crawl_run.id, job_id=crawl_job.id)
        )

    @validate_permissions(Permission.WEBSITES)
    async def create_website(self, website_create_req: WebsiteCreateRequest):

        website_create = WebsiteCreate(
            **website_create_req.model_dump(),
            user_id=self.user.id,
            tenant_id=self.user.tenant_id,
            embedding_model_id=website_create_req.embedding_model.id,
        )

        website = await self.repo.add(website_create)

        crawl_run = await self._crawl_website(website)
        website.latest_crawl = crawl_run

        return website

    @validate_permissions(Permission.WEBSITES)
    async def crawl_website(self, website_id: UUID):
        # MIT License

        website = await self.get_website(website_id)

        if website.latest_crawl.status in [Status.QUEUED, Status.IN_PROGRESS]:
            raise CrawlAlreadyRunningException()

        return await self._crawl_website(website)

    async def create_space_website(
        self,
        url: str,
        space_id: UUID,
        download_files: bool,
        crawl_type: CrawlType,
        update_interval: UpdateInterval,
        name: Optional[str] = None,
        embedding_model_id: Optional[UUID] = None,
    ):
        space = await self.space_service.get_space(space_id)
        actor = self.actor_manager.get_space_actor_from_space(space=space)

        if not actor.can_create_websites():
            raise UnauthorizedException(
                "User does not have permission to create websites in this space"
            )

        if embedding_model_id is None:
            if space.is_personal():
                embedding_model = (
                    await self.ai_models_service.get_latest_available_embedding_model()
                )
            else:
                embedding_model = space.get_latest_embedding_model()

            if embedding_model is None:
                raise BadRequestException(
                    "Can not create a website in a space that does not have "
                    "an embedding model enabled"
                )

            embedding_model_id = embedding_model.id

        elif not space.is_embedding_model_in_space(embedding_model_id):
            raise UnauthorizedException("Embedding model is not available in the space")

        website_create = WebsiteCreate(
            space_id=space_id,
            name=name,
            url=url,
            download_files=download_files,
            crawl_type=crawl_type,
            update_interval=update_interval,
            user_id=self.user.id,
            tenant_id=self.user.tenant_id,
            embedding_model_id=embedding_model_id,
        )

        website = await self.repo.add(website_create)

        crawl_run = await self._crawl_website(website)
        website.latest_crawl = crawl_run

        return website

    async def get_website(self, id: UUID) -> Website:
        website = await self.repo.get(id)

        self._validate(website)
        space = await self.space_service.get_space(website.space_id)
        actor = self.actor_manager.get_space_actor_from_space(space=space)

        if not actor.can_read_websites():
            raise UnauthorizedException()

        return website

    async def get_websites_by_ids(self, ids: list[UUID]) -> list[Website]:
        websites = await self.repo.get_by_ids(ids)

        for website in websites:
            self._validate(website)
            space = await self.space_service.get_space(website.space_id)
            actor = self.actor_manager.get_space_actor_from_space(space=space)

            if not actor.can_read_websites():
                raise UnauthorizedException()

        return websites

    async def get_websites(self, by_tenant: bool = False) -> list[Website]:
        if by_tenant:
            validate_permission(self.user, permission=Permission.ADMIN)
            websites = await self.repo.get_by_tenant(self.user.tenant.id)
        else:
            websites = await self.repo.get_by_user(self.user.id)

        return websites

    async def update_website(
        self, website_update_req: WebsiteUpdateRequest, website_id: UUID
    ):
        website_update = WebsiteUpdate(
            **website_update_req.model_dump(exclude_unset=True), id=website_id
        )
        website = await self.repo.update(website_update)

        self._validate(website)
        space = await self.space_service.get_space(website.space_id)
        actor = self.actor_manager.get_space_actor_from_space(space=space)

        if not actor.can_edit_websites():
            raise UnauthorizedException()

        return website

    async def update_website_size(self, website_id: UUID):
        return await self.repo.update_website_size(website_id=website_id)

    async def delete_website(self, website_id: UUID):
        # Runs validation
        website = await self.get_website(website_id)

        space = await self.space_service.get_space(website.space_id)
        actor = self.actor_manager.get_space_actor_from_space(space=space)

        if not actor.can_delete_websites():
            raise UnauthorizedException()

        return await self.repo.delete(website_id)

    async def get_crawl_runs(self, website_id: UUID):
        website = await self.get_website(website_id)
        runs = await self.crawl_run_repo.get_by_website(website.id)

        for run in runs:
            self._validate(run)

        return runs

    async def get_crawl_run(self, id: UUID):
        run = await self.crawl_run_repo.get(id)

        self._validate(run)

        return run

    async def move_website_to_space(
        self, website_id: UUID, space_id: UUID, assistant_ids: list[UUID] = []
    ):
        website = await self.get_website(website_id)
        target_space = await self.space_service.get_space(space_id)
        source_space = await self.space_service.get_space(website.space_id)
        target_space_actor = self.actor_manager.get_space_actor_from_space(target_space)
        source_space_actor = self.actor_manager.get_space_actor_from_space(source_space)

        if not source_space_actor.can_delete_websites():
            raise UnauthorizedException(
                "User does not have permission to move website from space"
            )

        if not target_space_actor.can_create_websites():
            raise UnauthorizedException(
                "User does not have permission to create websites in the space"
            )

        if not target_space.is_embedding_model_in_space(website.embedding_model_id):
            raise BadRequestException(
                f"Space does not have embedding model {website.embedding_model.name} enabled."
            )

        await self.repo.add_website_to_space(website_id=website_id, space_id=space_id)
        await self.repo.remove_website_from_all_assistants(
            website_id=website_id, assistant_ids=assistant_ids
        )
