from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.incident import IncidentCreate, IncidentResponse
from app.services.incident_service import (
    create_incident,
    get_incidents,
    get_incident,
    delete_incident,
    update_incident
)

router = APIRouter()


@router.post("/", response_model=IncidentResponse)
def create_incident_endpoint(
    incident: IncidentCreate,
    db: Session = Depends(get_db)
):
    return create_incident(db, incident)


@router.get("/", response_model=list[IncidentResponse])
def get_incidents_endpoint(
    db: Session = Depends(get_db)
):
    return get_incidents(db)


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident_endpoint(
    incident_id: int,
    db: Session = Depends(get_db)
):
    return get_incident(db, incident_id)

@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident_endpoint(
    incident_id: int,
    incident: IncidentCreate,
    db: Session = Depends(get_db)
):
    return update_incident(db, incident_id, incident)


@router.delete("/{incident_id}", response_model=IncidentResponse)
def delete_incident_endpoint(
    incident_id: int,
    db: Session = Depends(get_db)
):
    return delete_incident(db, incident_id)