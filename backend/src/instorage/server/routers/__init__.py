from fastapi import APIRouter

from instorage.admin.admin_router import router as admin_router
from instorage.ai_models.completion_models.completion_models_router import (
    router as completion_models_router,
)
from instorage.ai_models.embedding_models.embedding_models_router import (
    router as embedding_models_router,
)
from instorage.allowed_origins.allowed_origin_router import (
    router as allowed_origins_router,
)
from instorage.analysis.analysis_router import router as analysis_router
from instorage.assistants.api.assistant_router import router as assistants_router
from instorage.dashboard.api.dashboard_router import router as dashboard_router
from instorage.files.file_router import router as files_router
from instorage.groups.group_router import router as groups_router
from instorage.info_blobs.info_blobs_router import router as info_blobs_router
from instorage.jobs.job_router import router as jobs_router
from instorage.limits.limit_router import router as limit_router
from instorage.logging.logging_router import router as logging_router
from instorage.main.config import get_settings
from instorage.services.service_router import router as services_router
from instorage.settings.settings_router import router as settings_router
from instorage.spaces.api.space_router import router as space_router
from instorage.user_groups.user_groups_router import router as user_groups_router
from instorage.users.user_router import router as users_router
from instorage.websites.website_router import router as website_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(info_blobs_router, prefix="/info-blobs", tags=["info-blobs"])
router.include_router(groups_router, prefix="/groups", tags=["groups"])
router.include_router(settings_router, prefix="/settings", tags=["settings"])
router.include_router(assistants_router, prefix="/assistants", tags=["assistants"])
router.include_router(services_router, prefix="/services", tags=["services"])
router.include_router(logging_router, prefix="/logging", tags=["logging"])
router.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
router.include_router(admin_router, prefix="/admin", tags=["admin"])
router.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
router.include_router(user_groups_router, prefix="/user-groups", tags=["user-groups"])
router.include_router(
    allowed_origins_router, prefix="/allowed-origins", tags=["allowed-origins"]
)
router.include_router(
    completion_models_router, prefix="/completion-models", tags=["completion-models"]
)
router.include_router(
    embedding_models_router, prefix="/embedding-models", tags=["embedding-models"]
)
router.include_router(files_router, prefix="/files", tags=["files"])
router.include_router(limit_router, prefix="/limits", tags=["limits"])
router.include_router(space_router, prefix="/spaces", tags=["spaces"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
router.include_router(website_router, prefix="/websites", tags=["websites"])


if get_settings().using_intric_proprietary:
    from instorage_prop.prop_routers import include_prop_routers

    include_prop_routers(router)

if get_settings().using_access_management:
    from instorage.roles.roles_router import router as roles_router

    router.include_router(roles_router, prefix="/roles", tags=["roles"])
