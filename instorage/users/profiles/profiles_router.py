from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from instorage.authentication.auth_dependencies import get_current_active_user
from instorage.server.dependencies.db import get_repository
from instorage.users.profiles.profile import ProfilePublic, ProfileUpdate
from instorage.users.profiles.profiles_repo import ProfilesRepository
from instorage.users.user import UserInDB

router = APIRouter()


@router.get(
    "/{username}/",
    response_model=ProfilePublic,
    name="profiles:get-profile-by-username",
    include_in_schema=False,
)
async def get_profile_by_username(
    username: str = Path(..., min_length=3, pattern="^[a-zA-Z0-9_-]+$"),
    current_user: UserInDB = Depends(get_current_active_user),
    profiles_repo: ProfilesRepository = Depends(get_repository(ProfilesRepository)),
) -> ProfilePublic:
    profile = await profiles_repo.get_profile_by_username(username=username)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No profile found with that username.",
        )
    return profile


@router.put(
    "/me/",
    response_model=ProfilePublic,
    name="profiles:update-own-profile",
    include_in_schema=False,
)
async def update_own_profile(
    profile_update: ProfileUpdate = Body(..., embed=True),
    current_user: UserInDB = Depends(get_current_active_user),
    profiles_repo: ProfilesRepository = Depends(get_repository(ProfilesRepository)),
) -> ProfilePublic:
    updated_profile = await profiles_repo.update_profile(
        profile_update=profile_update, requesting_user=current_user
    )
    return updated_profile
