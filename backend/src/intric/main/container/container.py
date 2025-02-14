from dependency_injector import containers, providers

from intric.actors import ActorFactory, ActorManager
from intric.admin.admin_service import AdminService
from intric.admin.quota_service import QuotaService
from intric.ai_models.ai_models_service import AIModelsService
from intric.ai_models.completion_models.completion_model import (
    CompletionModel,
    CompletionModelFamily,
)
from intric.ai_models.completion_models.completion_model_adapters import (
    AzureOpenAIModelAdapter,
    ClaudeModelAdapter,
    OpenAIModelAdapter,
    VLMMModelAdapter,
)
from intric.ai_models.completion_models.completion_models_repo import (
    CompletionModelsRepository,
)
from intric.ai_models.completion_models.completion_service import (
    CompletionService,
    CompletionServiceFactory,
)
from intric.ai_models.completion_models.context_builder import ContextBuilder
from intric.ai_models.embedding_models.datastore.datastore import Datastore
from intric.ai_models.embedding_models.embedding_model import (
    EmbeddingModel,
    EmbeddingModelFamily,
)
from intric.ai_models.embedding_models.embedding_model_adapters import (
    InfinityAdapter,
    OpenAIEmbeddingAdapter,
)
from intric.ai_models.embedding_models.embedding_models_repo import (
    EmbeddingModelsRepository,
)
from intric.ai_models.transcription_models.model_adapters.whisper import (
    OpenAISTTModelAdapter,
)
from intric.allowed_origins.allowed_origin_repo import AllowedOriginRepository
from intric.allowed_origins.allowed_origin_service import AllowedOriginService
from intric.analysis.analysis_repo import AnalysisRepository
from intric.analysis.analysis_service import AnalysisService
from intric.apps import (
    AppAssembler,
    AppFactory,
    AppRepository,
    AppRunAssembler,
    AppRunFactory,
    AppRunRepository,
    AppRunService,
    AppService,
)
from intric.assistants.api.assistant_assembler import AssistantAssembler
from intric.assistants.assistant_factory import AssistantFactory
from intric.assistants.assistant_repo import AssistantRepository
from intric.assistants.assistant_service import AssistantService
from intric.assistants.references import ReferencesService
from intric.authentication.api_key_repo import ApiKeysRepository
from intric.authentication.auth_service import AuthService
from intric.completion_models.application import CompletionModelCRUDService
from intric.completion_models.domain import CompletionModelRepository
from intric.completion_models.presentation import CompletionModelAssembler
from intric.crawler.crawler import Crawler
from intric.database.database import AsyncSession
from intric.files.file_protocol import FileProtocol
from intric.files.file_repo import FileRepository
from intric.files.file_service import FileService
from intric.files.file_size_service import FileSizeService
from intric.files.image import ImageExtractor
from intric.files.text import TextExtractor
from intric.files.transcriber import Transcriber
from intric.groups.group_repo import GroupRepository
from intric.groups.group_service import GroupService
from intric.info_blobs.info_blob_chunk_repo import InfoBlobChunkRepo
from intric.info_blobs.info_blob_repo import InfoBlobRepository
from intric.info_blobs.info_blob_service import InfoBlobService
from intric.info_blobs.text_processor import TextProcessor
from intric.integration.application.integration_service import IntegrationService
from intric.integration.application.tenant_integration_service import (
    TenantIntegrationService,
)
from intric.integration.application.user_integration_service import (
    UserIntegrationService,
)
from intric.integration.domain.repositories.integration_repo import (
    IntegrationRepository,
)
from intric.integration.domain.repositories.tenant_integration_repo import (
    TenantIntegrationRepository,
)
from intric.integration.domain.repositories.user_integration_repo import (
    UserIntegrationRepository,
)
from intric.integration.presentation.assemblers.integration_assembler import (
    IntegrationAssembler,
)
from intric.integration.presentation.assemblers.tenant_integration_assembler import (
    TenantIntegrationAssembler,
)
from intric.integration.presentation.assemblers.user_integration_assembler import (
    UserIntegrationAssembler,
)
from intric.jobs.job_repo import JobRepository
from intric.jobs.job_service import JobService
from intric.jobs.task_service import TaskService
from intric.limits.limit_service import LimitService
from intric.main.aiohttp_client import aiohttp_client
from intric.main.config import SETTINGS
from intric.modules.module_repo import ModuleRepository
from intric.predefined_roles.predefined_role_service import PredefinedRolesService
from intric.predefined_roles.predefined_roles_repo import PredefinedRolesRepository
from intric.prompts.api.prompt_assembler import PromptAssembler
from intric.prompts.prompt_factory import PromptFactory
from intric.prompts.prompt_repo import PromptRepository
from intric.prompts.prompt_service import PromptService
from intric.questions.questions_repo import QuestionRepository
from intric.roles.roles_repo import RolesRepository
from intric.roles.roles_service import RolesService
from intric.services.service_repo import ServiceRepository
from intric.services.service_runner import ServiceRunner
from intric.services.service_service import ServiceService
from intric.sessions.session_service import SessionService
from intric.sessions.sessions_repo import SessionRepository
from intric.settings.setting_service import SettingService
from intric.settings.settings_repo import SettingsRepository
from intric.spaces.api.space_assembler import SpaceAssembler
from intric.spaces.space_factory import SpaceFactory
from intric.spaces.space_init_service import SpaceInitService
from intric.spaces.space_repo import SpaceRepository
from intric.spaces.space_service import SpaceService
from intric.storage.application.storage_services import StorageInfoService
from intric.storage.domain.storage_factory import StorageInfoFactory
from intric.storage.domain.storage_repo import StorageInfoRepository
from intric.storage.presentation.storage_assembler import StorageInfoAssembler
from intric.templates.api.templates_assembler import TemplateAssembler
from intric.templates.app_template.api.app_template_assembler import (
    AppTemplateAssembler,
)
from intric.templates.app_template.app_template_factory import AppTemplateFactory
from intric.templates.app_template.app_template_repo import AppTemplateRepository
from intric.templates.app_template.app_template_service import AppTemplateService
from intric.templates.assistant_template.api.assistant_template_assembler import (
    AssistantTemplateAssembler,
)
from intric.templates.assistant_template.assistant_template_factory import (
    AssistantTemplateFactory,
)
from intric.templates.assistant_template.assistant_template_repo import (
    AssistantTemplateRepository,
)
from intric.templates.assistant_template.assistant_template_service import (
    AssistantTemplateService,
)
from intric.templates.templates_service import TemplateService
from intric.tenants.tenant import TenantInDB
from intric.tenants.tenant_repo import TenantRepository
from intric.tenants.tenant_service import TenantService
from intric.user_groups.user_groups_repo import UserGroupsRepository
from intric.user_groups.user_groups_service import UserGroupsService
from intric.users.user import UserInDB
from intric.users.user_assembler import UserAssembler
from intric.users.user_repo import UsersRepository
from intric.users.user_service import UserService
from intric.websites.crawl_dependencies.crawl_runs_repo import CrawlRunRepository
from intric.websites.website_assembler import WebsiteAssembler
from intric.websites.website_repo import WebsiteRepository
from intric.websites.website_service import WebsiteService
from intric.worker.task_manager import TaskManager
from intric.workflows.step_repo import StepRepository

if SETTINGS.using_intric_proprietary:
    from intric_prop.apps.publish_app_service import PublishAppService
    from intric_prop.assistants.publish_assistant_service import PublishAssistantService
    from intric_prop.authentication.iam_client import ZitadelClient
    from intric_prop.sysadmin.sysadmin_service import SysAdminService
    from intric_prop.users.user_provision_service import UserProvisioningService
    from intric_prop.users.user_service import UserService as PropUserService
    from intric_prop.widgets.widget_repo import WidgetRepository
    from intric_prop.widgets.widget_service import WidgetService


class Container(containers.DeclarativeContainer):
    __self__ = providers.Self()

    # Configuration
    config = providers.Configuration()

    # Objects
    session = providers.Dependency(instance_of=AsyncSession)
    user = providers.Dependency(instance_of=UserInDB)
    tenant = providers.Dependency(instance_of=TenantInDB)
    embedding_model = providers.Dependency(instance_of=EmbeddingModel)
    completion_model = providers.Dependency(instance_of=CompletionModel)
    aiohttp_client = providers.Object(aiohttp_client)

    # Factories
    space_factory = providers.Factory(SpaceFactory)
    storage_info_factory = providers.Factory(StorageInfoFactory)
    prompt_factory = providers.Factory(PromptFactory)
    assistant_template_factory = providers.Factory(AssistantTemplateFactory)
    assistant_factory = providers.Factory(
        AssistantFactory,
        container=__self__,
        prompt_factory=prompt_factory,
        assistant_template_factory=assistant_template_factory,
    )
    completion_service_factory = providers.Factory(
        CompletionServiceFactory, container=__self__
    )
    app_run_factory = providers.Factory(AppRunFactory)
    app_template_factory = providers.Factory(AppTemplateFactory)
    actor_factory = providers.Factory(ActorFactory)

    # Managers
    actor_manager = providers.Factory(ActorManager, user=user, factory=actor_factory)

    # Assemblers
    prompt_assembler = providers.Factory(PromptAssembler, user=user)
    assistant_assembler = providers.Factory(
        AssistantAssembler, user=user, prompt_assembler=prompt_assembler
    )
    completion_model_assembler = providers.Factory(CompletionModelAssembler)
    space_assembler = providers.Factory(
        SpaceAssembler,
        user=user,
        assistant_assembler=assistant_assembler,
        completion_model_assembler=completion_model_assembler,
        actor_manager=actor_manager,
    )
    storage_assembler = providers.Factory(StorageInfoAssembler)
    app_assembler = providers.Factory(AppAssembler, prompt_assembler=prompt_assembler)
    app_run_assembler = providers.Factory(AppRunAssembler)
    app_template_assembler = providers.Factory(AppTemplateAssembler)
    assistant_template_assembler = providers.Factory(AssistantTemplateAssembler)
    template_assembler = providers.Factory(
        TemplateAssembler,
        app_assembler=AppTemplateAssembler,
        assistant_assembler=AssistantTemplateAssembler,
    )
    website_assembler = providers.Factory(WebsiteAssembler)

    user_assembler = providers.Factory(UserAssembler)

    integration_assembler = providers.Factory(IntegrationAssembler)
    tenant_integration_assembler = providers.Factory(TenantIntegrationAssembler)
    user_integration_assembler = providers.Factory(UserIntegrationAssembler)

    # Repositories
    user_repo = providers.Factory(UsersRepository, session=session)
    tenant_repo = providers.Factory(TenantRepository, session=session)
    settings_repo = providers.Factory(SettingsRepository, session=session)
    tenant_repo = providers.Factory(TenantRepository, session=session)
    prompt_repo = providers.Factory(
        PromptRepository, session=session, factory=prompt_factory
    )
    assistant_repo = providers.Factory(
        AssistantRepository, session=session, factory=assistant_factory
    )
    app_factory = providers.Factory(
        AppFactory, app_template_factory=app_template_factory
    )
    app_repo = providers.Factory(
        AppRepository,
        session=session,
        factory=app_factory,
        prompt_repo=prompt_repo,
    )
    app_run_repo = providers.Factory(
        AppRunRepository, session=session, factory=app_run_factory
    )

    api_key_repo = providers.Factory(ApiKeysRepository, session=session)
    group_repo = providers.Factory(GroupRepository, session=session)
    info_blob_repo = providers.Factory(InfoBlobRepository, session=session)
    job_repo = providers.Factory(JobRepository, session=session)
    allowed_origin_repo = providers.Factory(AllowedOriginRepository, session=session)
    predefined_roles_repo = providers.Factory(
        PredefinedRolesRepository, session=session
    )
    role_repo = providers.Factory(RolesRepository, session=session)
    completion_model_repo = providers.Factory(
        CompletionModelsRepository, session=session
    )
    integration_repo = providers.Factory(IntegrationRepository, session=session)
    tenant_integration_repo = providers.Factory(
        TenantIntegrationRepository, session=session
    )
    user_integration_repo = providers.Factory(
        UserIntegrationRepository, session=session
    )

    # TODO: rename when the first repo is not used anymore
    completion_model_repo2 = providers.Factory(
        CompletionModelRepository, session=session, user=user
    )
    embedding_model_repo = providers.Factory(EmbeddingModelsRepository, session=session)
    info_blob_chunk_repo = providers.Factory(InfoBlobChunkRepo, session=session)
    service_repo = providers.Factory(ServiceRepository, session=session)
    step_repo = providers.Factory(StepRepository, session=session)
    user_groups_repo = providers.Factory(UserGroupsRepository, session=session)
    analysis_repo = providers.Factory(AnalysisRepository, session=session)
    session_repo = providers.Factory(SessionRepository, session=session)
    question_repo = providers.Factory(QuestionRepository, session=session)
    file_repo = providers.Factory(FileRepository, session=session)
    website_repo = providers.Factory(WebsiteRepository, session=session)
    crawl_run_repo = providers.Factory(CrawlRunRepository, session=session)

    storage_repo = providers.Factory(
        StorageInfoRepository, user=user, session=session, factory=storage_info_factory
    )
    space_repo = providers.Factory(
        SpaceRepository,
        user=user,
        factory=space_factory,
        session=session,
        assistant_repo=assistant_repo,
        app_repo=app_repo,
    )
    app_template_repo = providers.Factory(
        AppTemplateRepository, factory=app_template_factory, session=session
    )
    assistant_template_repo = providers.Factory(
        AssistantTemplateRepository, factory=assistant_template_factory, session=session
    )

    module_repo = providers.Factory(ModuleRepository, session=session)

    # Completion model adapters
    openai_model_adapter = providers.Factory(OpenAIModelAdapter, model=completion_model)
    vllm_model_adapter = providers.Factory(VLMMModelAdapter, model=completion_model)
    claude_model_adapter = providers.Factory(ClaudeModelAdapter, model=completion_model)
    azure_model_adapter = providers.Factory(
        AzureOpenAIModelAdapter, model=completion_model
    )
    completion_model_selector = providers.Selector(
        config.completion_model,
        **{
            CompletionModelFamily.OPEN_AI.value: openai_model_adapter,
            CompletionModelFamily.VLLM.value: vllm_model_adapter,
            CompletionModelFamily.CLAUDE.value: claude_model_adapter,
            CompletionModelFamily.AZURE.value: azure_model_adapter,
        },
    )

    # Embedding model adapters
    multilingual_adapter = providers.Factory(InfinityAdapter, model=embedding_model)
    openai_embedding_adapter = providers.Factory(
        OpenAIEmbeddingAdapter, model=embedding_model
    )
    embedding_model_selector = providers.Selector(
        config.embedding_model,
        **{
            EmbeddingModelFamily.E5.value: multilingual_adapter,
            EmbeddingModelFamily.OPEN_AI.value: openai_embedding_adapter,
        },
    )

    # Speech-to-text model adapter
    openai_stt_model_adapter = providers.Factory(OpenAISTTModelAdapter)

    # Datastore
    datastore = providers.Factory(
        Datastore,
        user=user,
        embedding_model_adapter=embedding_model_selector,
        info_blob_chunk_repo=info_blob_chunk_repo,
    )
    text_extractor = providers.Factory(TextExtractor)
    image_extractor = providers.Factory(ImageExtractor)

    # Services
    ai_models_service = providers.Factory(
        AIModelsService,
        user=user,
        embedding_model_repo=embedding_model_repo,
        completion_model_repo=completion_model_repo,
        tenant_repo=tenant_repo,
    )
    completion_model_crud_service = providers.Factory(
        CompletionModelCRUDService,
        user=user,
        completion_model_repo=completion_model_repo2,
    )
    auth_service = providers.Factory(
        AuthService,
        api_key_repo=api_key_repo,
    )
    tenant_service = providers.Factory(
        TenantService, repo=tenant_repo, completion_model_repo=completion_model_repo
    )
    user_service = providers.Factory(
        UserService,
        user_repo=user_repo,
        auth_service=auth_service,
        settings_repo=settings_repo,
        tenant_repo=tenant_repo,
        assistant_repo=assistant_repo,
        predefined_roles_repo=predefined_roles_repo,
        info_blob_repo=info_blob_repo,
    )
    space_service = providers.Factory(
        SpaceService,
        user=user,
        repo=space_repo,
        factory=space_factory,
        user_repo=user_repo,
        ai_models_service=ai_models_service,
        completion_model_crud_service=completion_model_crud_service,
        actor_manager=actor_manager,
    )
    storage_service = providers.Factory(StorageInfoService, repo=storage_repo)
    job_service = providers.Factory(
        JobService,
        user=user,
        job_repo=job_repo,
    )
    file_size_service = providers.Factory(
        FileSizeService,
    )
    task_service = providers.Factory(
        TaskService,
        user=user,
        file_size_service=file_size_service,
        job_service=job_service,
    )
    group_service = providers.Factory(
        GroupService,
        user=user,
        repo=group_repo,
        space_repo=space_repo,
        tenant_repo=tenant_repo,
        info_blob_repo=info_blob_repo,
        ai_models_service=ai_models_service,
        space_service=space_service,
        actor_manager=actor_manager,
        task_service=task_service,
    )
    quota_service = providers.Factory(
        QuotaService, user=user, info_blob_repo=info_blob_repo
    )
    allowed_origin_service = providers.Factory(
        AllowedOriginService,
        user=user,
        repo=allowed_origin_repo,
    )
    predefined_role_service = providers.Factory(
        PredefinedRolesService, repo=predefined_roles_repo
    )
    role_service = providers.Factory(RolesService, user=user, repo=role_repo)
    settings_service = providers.Factory(
        SettingService,
        user=user,
        repo=settings_repo,
        ai_models_service=ai_models_service,
    )
    website_service = providers.Factory(
        WebsiteService,
        user=user,
        repo=website_repo,
        task_service=task_service,
        ai_models_service=ai_models_service,
        crawl_run_repo=crawl_run_repo,
        space_service=space_service,
        actor_manager=actor_manager,
    )
    info_blob_service = providers.Factory(
        InfoBlobService,
        repo=info_blob_repo,
        space_repo=space_repo,
        user=user,
        quota_service=quota_service,
        website_service=website_service,
        group_service=group_service,
        space_service=space_service,
        actor_manager=actor_manager,
    )
    prompt_service = providers.Factory(
        PromptService, user=user, repo=prompt_repo, factory=prompt_factory
    )
    file_protocol = providers.Factory(
        FileProtocol,
        file_size_service=file_size_service,
        text_extractor=text_extractor,
        image_extractor=image_extractor,
    )
    file_service = providers.Factory(
        FileService,
        user=user,
        repo=file_repo,
        protocol=file_protocol,
    )
    assistant_template_service = providers.Factory(
        AssistantTemplateService,
        repo=assistant_template_repo,
        factory=assistant_template_factory,
    )
    session_service = providers.Factory(
        SessionService,
        user=user,
        question_repo=question_repo,
        session_repo=session_repo,
    )
    assistant_service = providers.Factory(
        AssistantService,
        user=user,
        repo=assistant_repo,
        space_repo=space_repo,
        auth_service=auth_service,
        service_repo=service_repo,
        step_repo=step_repo,
        completion_model_crud_service=completion_model_crud_service,
        group_service=group_service,
        website_service=website_service,
        space_service=space_service,
        factory=assistant_factory,
        prompt_service=prompt_service,
        file_service=file_service,
        assistant_template_service=assistant_template_service,
        session_service=session_service,
        actor_manager=actor_manager,
    )
    app_template_service = providers.Factory(
        AppTemplateService,
        repo=app_template_repo,
        factory=app_template_factory,
    )

    template_service = providers.Factory(
        TemplateService,
        app_service=app_template_service,
        assistant_service=assistant_template_service,
    )

    space_init_service = providers.Factory(
        SpaceInitService,
        user=user,
        space_service=space_service,
        assistant_service=assistant_service,
        space_repo=space_repo,
    )
    user_group_service = providers.Factory(
        UserGroupsService, user=user, repo=user_groups_repo
    )
    admin_service = providers.Factory(
        AdminService,
        user=user,
        user_repo=user_repo,
        tenant_repo=tenant_repo,
        user_service=user_service,
    )
    settings_service = providers.Factory(
        SettingService,
        user=user,
        repo=settings_repo,
        ai_models_service=ai_models_service,
    )
    service_service = providers.Factory(
        ServiceService,
        repo=service_repo,
        space_repo=space_repo,
        question_repo=question_repo,
        group_service=group_service,
        user=user,
        completion_model_crud_service=completion_model_crud_service,
        space_service=space_service,
        actor_manager=actor_manager,
    )
    limit_service = providers.Factory(LimitService)

    integration_service = providers.Factory(
        IntegrationService, integration_repo=integration_repo
    )
    tenant_integration_service = providers.Factory(
        TenantIntegrationService, tenant_integration_repo=tenant_integration_repo
    )
    user_integration_service = providers.Factory(
        UserIntegrationService, user_integration_repo=user_integration_repo
    )

    # Completion
    context_builder = providers.Factory(ContextBuilder)
    completion_service = providers.Factory(
        CompletionService,
        context_builder=context_builder,
        model_adapter=completion_model_selector,
    )
    references_service = providers.Factory(
        ReferencesService,
        info_blobs_repo=info_blob_repo,
        datastore=datastore,
    )
    service_runner = providers.Factory(
        ServiceRunner,
        user=user,
        completion_service=completion_service,
        references_service=references_service,
        question_repo=question_repo,
        file_service=file_service,
    )
    analysis_service = providers.Factory(
        AnalysisService,
        user=user,
        repo=analysis_repo,
        assistant_service=assistant_service,
        session_repo=session_repo,
        question_repo=question_repo,
        space_service=space_service,
    )

    # Worker
    task_manager = providers.Factory(
        TaskManager,
        user=user,
        session=session,
        job_service=job_service,
    )
    text_processor = providers.Factory(
        TextProcessor,
        user=user,
        extractor=text_extractor,
        datastore=datastore,
        info_blob_service=info_blob_service,
        session=session,
    )
    transcriber = providers.Factory(
        Transcriber,
        adapter=openai_stt_model_adapter,
    )
    crawler = providers.Factory(Crawler)

    # Worker dependent services
    app_service = providers.Factory(
        AppService,
        user=user,
        repo=app_repo,
        space_repo=space_repo,
        factory=app_factory,
        completion_model_crud_service=completion_model_crud_service,
        file_service=file_service,
        prompt_service=prompt_service,
        completion_service_factory=completion_service_factory,
        transcriber=transcriber,
        app_template_service=app_template_service,
        group_service=group_service,
        actor_manager=actor_manager,
    )
    app_run_service = providers.Factory(
        AppRunService,
        user=user,
        repo=app_run_repo,
        factory=app_run_factory,
        app_service=app_service,
        file_service=file_service,
        job_service=job_service,
    )

    if SETTINGS.using_intric_proprietary:
        # Clients
        zitadel_client = providers.Factory(ZitadelClient, aiohttp_client=aiohttp_client)

        # Repositories
        widget_repo = providers.Factory(WidgetRepository, session=session)
        app_run_repo = providers.Factory(
            AppRunRepository, session=session, factory=app_run_factory
        )

        # Services
        user_provision_service = providers.Factory(
            UserProvisioningService,
            user_repo=user_repo,
            iam_client=zitadel_client,
            tenant_repo=tenant_repo,
            predefined_roles_repo=predefined_roles_repo,
        )
        sysadmin_service = providers.Factory(SysAdminService)
        widget_service = providers.Factory(
            WidgetService,
            user=user,
            widget_repo=widget_repo,
            assistant_service=assistant_service,
            tenant_repo=tenant_repo,
        )
        prop_user_service = providers.Factory(
            PropUserService,
            user=user,
            user_repo=user_repo,
            space_service=space_service,
        )
        publish_app_service = providers.Factory(
            PublishAppService,
            repo=app_repo,
            space_repo=space_repo,
            actor_manager=actor_manager,
        )
        publish_assistant_service = providers.Factory(
            PublishAssistantService,
            repo=assistant_repo,
            space_repo=space_repo,
            actor_manager=actor_manager,
        )
