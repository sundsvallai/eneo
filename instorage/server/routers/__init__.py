from fastapi import APIRouter

from instorage.admin.admin_router import router as admin_router
from instorage.allowed_origins.allowed_origin_router import (
    router as allowed_origins_router,
)
from instorage.analysis.analysis_router import router as analysis_router
from instorage.assistants.assistant_router import router as assistants_router
from instorage.groups.group_router import router as groups_router
from instorage.info_blobs.info_blobs_router import router as info_blobs_router
from instorage.jobs.job_router import router as jobs_router
from instorage.logging.logging_router import router as logging_router
from instorage.main.config import get_settings
from instorage.modules.module_router import router as module_router
from instorage.services.service_router import router as services_router
from instorage.settings.settings_router import router as settings_router
from instorage.user_groups.user_groups_router import router as user_groups_router
from instorage.users.profiles.profiles_router import router as profiles_router
from instorage.users.user_router import router as users_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(info_blobs_router, prefix="/info-blobs", tags=["info-blobs"])
router.include_router(profiles_router, prefix="/profiles", tags=["profiles"])
router.include_router(groups_router, prefix="/groups", tags=["groups"])
router.include_router(settings_router, prefix="/settings", tags=["settings"])
router.include_router(assistants_router, prefix="/assistants", tags=["assistants"])
router.include_router(services_router, prefix="/services", tags=["services"])
router.include_router(logging_router, prefix="/logging", tags=["logging"])
router.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
router.include_router(admin_router, prefix="/admin", tags=["admin"])
router.include_router(module_router, prefix="/modules", tags=["modules"])
router.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
router.include_router(user_groups_router, prefix="/user-groups", tags=["user-groups"])
router.include_router(
    allowed_origins_router, prefix="/allowed-origins", tags=["allowed-origins"]
)

if get_settings().using_intric_proprietary:
    if get_settings().using_widgets:
        from instorage_prop.widgets.widget_router import router as widget_router

        router.include_router(widget_router, prefix="/widgets", tags=["widgets"])

    if get_settings().using_crawl:
        from instorage_prop.crawler.crawl_router import router as crawl_router

        router.include_router(crawl_router, prefix="/crawls", tags=["crawls"])

    from instorage_prop.sysadmin.sysadmin_router import router as sysadmin_router

    router.include_router(sysadmin_router, prefix="/sysadmin", tags=["sysadmin"])


if get_settings().using_access_management:
    from instorage.roles.roles_router import router as roles_router

    router.include_router(roles_router, prefix="/roles", tags=["roles"])
