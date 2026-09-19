from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1.health import router as health_router
from app.core.config import settings
from app.api.v1.scanners import router as scanner_router
from app.api.v1.branches import router as branch_router
from app.api.v1.incidents import router as incident_router
from app.api.v1.users import router as user_router
import logging
from app.core.logging_config import setup_logging

logger = logging.getLogger(__name__)

setup_logging()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unhandled exception while processing %s %s",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )


app.include_router(health_router, prefix="/api/v1")

app.include_router(
    scanner_router,
    prefix="/api/v1/scanners",
    tags=["Scanners"]
)

app.include_router(
    branch_router,
    prefix="/api/v1/branches",
    tags=["Branches"]
)

app.include_router(
    incident_router,
    prefix="/api/v1/incidents",
    tags=["Incidents"]
)

app.include_router(
    user_router,
    prefix="/api/v1/users",
    tags=["Users"]
)