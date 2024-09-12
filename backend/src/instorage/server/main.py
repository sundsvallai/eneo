import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from instorage.allowed_origins.get_origin_callback import get_origin
from instorage.authentication import auth_dependencies
from instorage.main import config
from instorage.main.logging import get_logger
from instorage.server import api_documentation
from instorage.server.dependencies.lifespan import lifespan
from instorage.server.exception_handlers import add_exception_handlers
from instorage.server.middleware.cors import CORSMiddleware
from instorage.server.models.api import VersionResponse
from instorage.server.routers import router as api_router

if config.get_settings().using_intric_proprietary:
    from instorage_prop.config import get_allowed_origins

logger = get_logger(__name__)


if config.get_settings().using_intric_proprietary:
    allowed_origins = get_allowed_origins()
else:
    allowed_origins = ["*"]


def get_application():
    app = FastAPI(
        title=api_documentation.TITLE,
        version=config.get_settings().app_version,
        summary=api_documentation.SUMMARY,
        openapi_tags=api_documentation.TAGS_METADATA,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        callback=get_origin,
    )

    app.include_router(api_router, prefix=config.get_settings().api_prefix)

    # Add handlers of all errors except 500
    add_exception_handlers(app)

    return app


app = get_application()


@app.exception_handler(500)
async def custom_http_500_exception_handler(request, exc):
    # CORS Headers are not set on an internal server error. This is confusing, and hard to debug.
    # Solving this like this response:
    #   https://github.com/tiangolo/fastapi/issues/775#issuecomment-723628299
    response = JSONResponse(status_code=500, content={"error": "Something went wrong"})

    origin = request.headers.get("origin")

    if origin:
        # Have the middleware do the heavy lifting for us to parse
        # all the config, then update our response headers
        cors = CORSMiddleware(
            app=app,
            allow_origins=allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            callback=get_origin,
        )

        # Logic directly from Starlette's CORSMiddleware:
        # https://github.com/encode/starlette/blob/master/starlette/middleware/cors.py#L152

        response.headers.update(cors.simple_headers)
        has_cookie = "cookie" in request.headers

        # If request includes any cookie headers, then we must respond
        # with the specific origin instead of '*'.
        if cors.allow_all_origins and has_cookie:
            response.headers["Access-Control-Allow-Origin"] = origin

        # If we only allow specific origins, then we have to mirror back
        # the Origin header in the response.
        elif not cors.allow_all_origins and await cors.is_allowed_origin(origin=origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers.add_vary_header("Origin")

    return response


@app.get("/version", dependencies=[Depends(auth_dependencies.get_current_active_user)])
async def get_version():
    return VersionResponse(version=config.get_settings().app_version)


def start():
    uvicorn.run(
        "instorage.server.main:app",
        host="0.0.0.0",
        port=8123,
        reload=True,
        reload_dirs="./src/",
    )
