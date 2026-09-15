from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from app.db.database import get_db
from app.schemas.incident import IncidentCreate, IncidentResponse, IncidentListResponse
from app.services.incident_service import (
    create_incident,
    get_incidents,
    get_incident,
    delete_incident,
    update_incident
)

from app.core.authorization import require_role
from app.core.roles import Role

router = APIRouter()


@router.post("/", response_model=IncidentResponse)
def create_incident_endpoint(
    incident: IncidentCreate,
    current_user=Depends(require_role(
        Role.ADMIN,
        Role.MANAGER,
    )),
    db: Session = Depends(get_db)
):
    return create_incident(db, incident)


@router.get("/", response_model=IncidentListResponse)
def get_incidents_endpoint(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    scanner_id: int | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    db: Session = Depends(get_db),
    current_user=Depends(require_role(
        Role.ADMIN,
        Role.MANAGER,
        Role.VIEWER
    ))
):
    return get_incidents(db,
        page=page,
        page_size=page_size,
        search=search,
        status=status,
        priority=priority,
        scanner_id=scanner_id,
        sort_by=sort_by,
        sort_order=sort_order)


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident_endpoint(
    incident_id: int,
    current_user=Depends(require_role(
        Role.ADMIN,
        Role.MANAGER,
        Role.VIEWER
    )),
    db: Session = Depends(get_db)
):
    return get_incident(db, incident_id)

@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident_endpoint(
    incident_id: int,
    incident: IncidentCreate,
    current_user=Depends(require_role(
        Role.ADMIN,
        Role.MANAGER,
    )),
    db: Session = Depends(get_db)
):
    return update_incident(db, incident_id, incident)


@router.delete("/{incident_id}", response_model=IncidentResponse)
def delete_incident_endpoint(
    incident_id: int,
    current_user=Depends(require_role(
        Role.ADMIN,
    )),
    db: Session = Depends(get_db)
):
    return delete_incident(db, incident_id)