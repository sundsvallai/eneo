import uuid

from fastapi import APIRouter, Body, Depends, HTTPException, Path

from instorage.admin.beta_keys.beta_key import (
    BetaKeyCreateRequest,
    BetaKeyCreateResponse,
    BetaKeyInDB,
    BetaKeyPublic,
)
from instorage.admin.beta_keys.beta_keys_repo import BetaKeyRepository
from instorage.server.dependencies import db

router = APIRouter()


BETA_KEYS_CREATE_ROUTE = "beta-keys:create"
BETA_KEYS_GET_ROUTE = "beta-keys:get"
BETA_KEYS_CONSUME_ROUTE = "beta-keys:consume"


@router.post(
    "",
    response_model=BetaKeyCreateResponse,
    name=BETA_KEYS_CREATE_ROUTE,
    include_in_schema=False,
)
async def create_beta_keys(
    request: BetaKeyCreateRequest = Body(...),
    beta_key_repo: BetaKeyRepository = Depends(db.get_repository(BetaKeyRepository)),
):
    beta_keys_to_create = [str(uuid.uuid4()) for _ in range(request.number_of_keys)]

    beta_keys_created: list[BetaKeyInDB] = [
        await beta_key_repo.create_beta_key(beta_key)
        for beta_key in beta_keys_to_create
    ]

    keys = [key.key for key in beta_keys_created]

    return BetaKeyCreateResponse(keys=keys)


@router.get(
    "/{key}",
    response_model=BetaKeyPublic,
    name=BETA_KEYS_GET_ROUTE,
    include_in_schema=False,
)
async def get_beta_key(
    key: str = Path(...),
    beta_key_repo: BetaKeyRepository = Depends(db.get_repository(BetaKeyRepository)),
):
    key_in_db = await beta_key_repo.get_beta_key(key)
    if key_in_db is None:
        raise HTTPException(status_code=404)

    return key_in_db


@router.get(
    "/consume/{key}",
    response_model=BetaKeyPublic,
    name=BETA_KEYS_CONSUME_ROUTE,
    include_in_schema=False,
)
async def consume_beta_key(
    key: str = Path(...),
    beta_key_repo: BetaKeyRepository = Depends(db.get_repository(BetaKeyRepository)),
):
    key_in_db = await beta_key_repo.get_beta_key(key)
    if key_in_db is None:
        raise HTTPException(status_code=404)
    elif key_in_db.used:
        raise HTTPException(status_code=403)

    consumed_key = await beta_key_repo.consume_beta_key(key)
    return consumed_key
