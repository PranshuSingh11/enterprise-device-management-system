from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.schemas.incident import IncidentCreate

from datetime import datetime,timezone
from fastapi import HTTPException


def create_incident(db: Session, incident_data: IncidentCreate):
    new_incident = Incident(
        title=incident_data.title,
        description=incident_data.description,
        status=incident_data.status,
        priority=incident_data.priority,
        scanner_id=incident_data.scanner_id,
        created_at=datetime.now(timezone.utc)
    )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    return new_incident


def get_incidents(db: Session):
    return db.query(Incident).all()


def get_incident(db: Session, incident_id: int):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident
    
    
def update_incident(
    db: Session,
    incident_id: int,
    incident_data: IncidentCreate
):
    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    incident.title = incident_data.title
    incident.description = incident_data.description
    incident.status = incident_data.status
    incident.priority = incident_data.priority
    incident.scanner_id = incident_data.scanner_id

    db.commit()
    db.refresh(incident)

    return incident


def delete_incident(db: Session, incident_id: int):
    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    db.delete(incident)
    db.commit()

    return incident