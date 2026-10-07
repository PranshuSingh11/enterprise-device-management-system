from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.scanner import Scanner
from app.models.incident import Incident


def get_dashboard_summary(db: Session) -> dict:
    total_scanners = (
        db.query(func.count(Scanner.id))
        .scalar()
        or 0
    )

    active_scanners = (
        db.query(func.count(Scanner.id))
        .filter(Scanner.status == "Active")
        .scalar()
        or 0
    )

    open_incidents = (
        db.query(func.count(Incident.id))
        .filter(Incident.status == "open")
        .scalar()
        or 0
    )

    critical_incidents = (
        db.query(func.count(Incident.id))
        .filter(Incident.priority == "critical")
        .scalar()
        or 0
    )

    return {
        "total_scanners": total_scanners,
        "active_scanners": active_scanners,
        "open_incidents": open_incidents,
        "critical_incidents": critical_incidents,
    }