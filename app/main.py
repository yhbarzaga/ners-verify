from typing import Callable, Union

from fastapi import FastAPI, Request, status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.api_v1.api import api_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    """Initialize ners api settings."""
    settings = get_settings()

    server = FastAPI(
        title=settings.project_name,
        openapi_url="/api/v1/openapi.json",
        summary="Application for track expenses not related to commercial transactions",
    )

    @server.middleware("http")
    async def catch_exceptions_middleware(
        request: Request, call_next: Callable
    ) -> Union[Callable, JSONResponse]:
        """Catch any possible unhandled exception."""
        try:
            return await call_next(request)  # type: ignore[no-any-return]
        except Exception as e:
            return JSONResponse(
                content={
                    "detail": f"InternalServerError - the following exception was raised: {repr(e)}"
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # Set all CORS enabled origins
    if settings.backend_cors_origins:
        server.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.backend_cors_origins],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    server.include_router(api_router, prefix="/api/v1")

    return server


app = create_app()
