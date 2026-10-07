from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.authorization import require_role
from app.core.roles import Role
from app.db.database import get_db
from app.schemas.dashboard import DashboardSummaryResponse
from app.services.dashboard_service import get_dashboard_summary


router = APIRouter()


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
)
def get_summary(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role(Role.ADMIN, Role.MANAGER, Role.VIEWER)
    ),
):
    return get_dashboard_summary(db)