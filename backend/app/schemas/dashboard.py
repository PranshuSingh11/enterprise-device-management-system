from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_scanners: int
    active_scanners: int
    open_incidents: int
    critical_incidents: int