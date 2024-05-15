import json
import logging
import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings
from starlette.config import Config  # Not sure we should keep using starlette for this
from starlette.datastructures import Secret

from instorage.ai_models.completion_models.llms import CompletionModelName
from instorage.definitions import ROOT_DIR

config = Config(".env")

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)

DATABASE_URL = config(
    "DATABASE_URL",
    default=f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}",  # noqa
)

MANIFEST_LOCATION = f"{ROOT_DIR}/.release-please-manifest.json"


def _set_app_version():
    with open(MANIFEST_LOCATION) as f:
        manifest_data = json.load(f)

    version = manifest_data["."]
    if os.environ.get("DEV", False):
        return f'{version}-dev'

    return version


class Settings(BaseSettings):
    app_version: str = _set_app_version()
    intric_super_api_key: str
    intric_super_duper_api_key: str
    multilingual_e5_large_url: str = "http://development.inoolabs.com:22015/predict"
    openai_api_key: str
    sync_database_url: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"  # noqa
    )
    database_url: str = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"  # noqa
    )
    test_database_url: str = f"{database_url}_test"
    sync_test_database_url: str = f"{sync_database_url}_test"
    testing: bool = False
    instorage_default_prompt: str = "You are a helpful assistant."
    mobilityguard_discovery_endpoint: Optional[str] = None
    mobilityguard_client_id: str = "intric"
    mobilityguard_client_secret: Optional[str] = None
    using_intric_proprietary: bool = True
    environment: str = "development"
    traces_sample_rate: float = 1.0
    sample_rate: float = 1.0
    redis_host: str = "localhost"
    redis_port: int = 6378

    # Crawl
    crawl_max_length: int = 60 * 60 * 4  # 4 hour crawls max
    closespider_itemcount: int = 20000
    obey_robots: bool = True
    autothrottle_enabled: bool = True
    using_crawl: bool = False

    # Access Management
    using_access_management: bool = False

    # Widgets
    using_widgets: bool = True


@lru_cache
def get_settings():
    return Settings()


def get_app_version():
    return get_settings().app_version


def get_api_prefix():
    # Prefix for API routes, like so: <API_PREFIX>/other/routes
    # Note the need for leading slash, but lack of trailing slash. An example entry would be "/api"
    return os.getenv("API_PREFIX", "/api/v1")


def get_api_key_length():
    # Length of API key, in bytes
    return os.getenv("API_KEY_LENGTH", 32)


def get_api_key_header_name():
    return os.getenv("API_KEY_HEADER_NAME", "api-key")


def get_jwt_audience():
    # We add this to the JWT, can be used like realm, or like a property for the FE
    return os.getenv("JWT_AUDIENCE", "beta")


def get_jwt_expiry_time_minutes():
    # How long it's going to last. No refresh tokens yet, so we set it to a week
    return int(os.getenv("JWT_EXPIRY_TIME", 7 * 24 * 60))


def get_jwt_algorithm():
    # Standard algo
    return os.getenv("JWT_ALGORITHM", "HS256")


def get_jwt_secret():
    # The secret we use to sign our JWT's
    return os.getenv("JWT_SECRET", "super-secret-jwt")


def get_jwt_token_prefix():
    # Prefix for HTTP Authorization headers
    return os.getenv("JWT_TOKEN_PREFIX", "Bearer ")


def get_gpt_sw3_api_key():
    # Key we use to authenticate ourselves with gpt-sw3-instruct
    return os.getenv("GPT_SW3_API_KEY")


def get_default_completion_model():
    # Which model to use if user has not made a choice
    return os.getenv("INSTORAGE_DEFAULT_COMPLETION_MODEL", CompletionModelName.CHATGPT)


def get_default_top_k():
    # Default number of info_blobs to send to the completion models
    return int(os.getenv("INSTORAGE_TOP_K", 30))


def get_default_prompt():
    return get_settings().instorage_default_prompt


def get_default_minimal_number_of_info_blobs():
    # Default number of minial info_blobs needed to fit in the context size
    # without raising exceptions
    return int(os.getenv("INSTORAGE_MINIMAL_TOP_K", 3))


def get_allow_all_cors_toggle():
    return bool(os.getenv("INTRIC_CORS_ALLOW_ALL", False))


def get_loglevel():
    loglevel = os.getenv("LOGLEVEL", "INFO")

    match loglevel:
        case "INFO":
            return logging.INFO
        case "WARNING":
            return logging.WARNING
        case "ERROR":
            return logging.ERROR
        case "CRITICAL":
            return logging.CRITICAL
        case "DEBUG":
            return logging.DEBUG
        case _:
            return logging.INFO
