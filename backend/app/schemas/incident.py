from datetime import datetime

from pydantic import BaseModel


class IncidentCreate(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    scanner_id: int


class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    scanner_id: int
    created_at: datetime
    resolved_at: datetime | None

    class Config:
        from_attributes = True
        
class IncidentListResponse(BaseModel):
    items: list[IncidentResponse]
    page: int
    page_size: int
    total: int
    total_pages: int