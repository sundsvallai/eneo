from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from instorage.main.exceptions import EXCEPTION_MAP


def add_exception_handlers(app: FastAPI):
    for exception, (status_code, error_message) in EXCEPTION_MAP.items():

        def handler(
            request: Request,
            exc,
            status_code: int = status_code,
            error_message: str = error_message,
        ):
            message = error_message or str(exc)
            return JSONResponse(status_code=status_code, content={"message": message})

        app.add_exception_handler(exception, handler)
