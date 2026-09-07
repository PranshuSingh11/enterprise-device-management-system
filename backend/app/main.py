from fastapi import FastAPI
from app.api.v1.health import router as health_router
from app.core.config import settings
from app.api.v1.scanners import router as scanner_router
from app.api.v1.branches import router as branch_router
from app.api.v1.incidents import router as incident_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
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