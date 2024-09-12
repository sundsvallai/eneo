from fastapi import Depends

from instorage.admin.quota_service import QuotaService
from instorage.authentication.auth_dependencies import get_current_active_user
from instorage.info_blobs.info_blob_repo import InfoBlobRepository
from instorage.server.dependencies.get_repository import get_repository
from instorage.users.user import UserInDB


async def get_quota_service(
    user: UserInDB = Depends(get_current_active_user),
    info_blob_repo: InfoBlobRepository = Depends(get_repository(InfoBlobRepository)),
):
    return QuotaService(user, info_blob_repo=info_blob_repo)
