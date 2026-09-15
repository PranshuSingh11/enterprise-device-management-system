from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.incident import Incident
from app.schemas.incident import IncidentCreate
from app.models.scanner import Scanner
from datetime import datetime,timezone
from fastapi import HTTPException

ALLOWED_STATUSES = {
    "open",
    "in_progress",
    "resolved",
    "closed"
}

ALLOWED_PRIORITIES = {
    "low",
    "medium",
    "high",
    "critical"
}

def create_incident(db: Session, incident_data: IncidentCreate):
    new_incident = Incident(
        title=incident_data.title,
        description=incident_data.description,
        status=incident_data.status,
        priority=incident_data.priority,
        scanner_id=incident_data.scanner_id,
        created_at=datetime.now(timezone.utc)
    )
    
    if incident_data.status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid incident status: {incident_data.status}"
        )

    if incident_data.priority not in ALLOWED_PRIORITIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid incident priority: {incident_data.priority}"
        )
    
    scanner = db.query(Scanner).filter(
    Scanner.id == incident_data.scanner_id
).first()

    if scanner is None:
        raise HTTPException(
            status_code=404,
            detail="Scanner not found"
        )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    return new_incident


ALLOWED_SORT_FIELDS = {
    "id",
    "title",
    "status",
    "priority",
    "scanner_id",
    "created_at"
}


def get_incidents(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    scanner_id: int | None = None,
    sort_by: str = "id",
    sort_order: str = "asc"
):
    query = db.query(Incident)

    if search:
        search_term = f"%{search}%"

        query = query.filter(
            or_(
                Incident.title.ilike(search_term),
                Incident.description.ilike(search_term)
            )
        )

    if status:
        query = query.filter(Incident.status == status)

    if priority:
        query = query.filter(Incident.priority == priority)

    if scanner_id:
        query = query.filter(Incident.scanner_id == scanner_id)

    if sort_by not in ALLOWED_SORT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field: {sort_by}"
        )

    if sort_order.lower() not in {"asc", "desc"}:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort order: {sort_order}"
        )

    sort_column = getattr(Incident, sort_by, Incident.id)

    if sort_order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    total = query.count()

    offset = (page - 1) * page_size

    incidents = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    total_pages = (total + page_size - 1) // page_size

    return {
        "items": incidents,
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages
    }

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
    
    if incident.status == "closed" and incident_data.status != "closed":
        raise HTTPException(
            status_code=400,
            detail="Closed incidents cannot be reopened"
        )
    
    if incident_data.status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid incident status: {incident_data.status}"
        )

    if incident_data.priority not in ALLOWED_PRIORITIES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid incident priority: {incident_data.priority}"
        )

 
    
    scanner = db.query(Scanner).filter(
    Scanner.id == incident_data.scanner_id
).first()

    if scanner is None:
        raise HTTPException(
            status_code=404,
            detail="Scanner not found"
        )

    if incident_data.status in {"resolved", "closed"}:
        incident.resolved_at = datetime.now(timezone.utc)
    else:
        incident.resolved_at = None

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