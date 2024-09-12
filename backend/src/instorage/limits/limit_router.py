from fastapi import APIRouter, Depends

from instorage.limits.limit import Limits
from instorage.limits.limit_factory import get_limit_service
from instorage.limits.limit_service import LimitService

router = APIRouter()


@router.get("/", response_model=Limits)
def get_limits(service: LimitService = Depends(get_limit_service)):
    return service.get_limits()
