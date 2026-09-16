from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Incident(Base):
    __tablename__ = "incidents"
    
    __table_args__ = (
    CheckConstraint(
        "status IN ('open', 'in_progress', 'resolved', 'closed')",
        name="ck_incidents_status"
    ),
    CheckConstraint(
        "priority IN ('low', 'medium', 'high', 'critical')",
        name="ck_incidents_priority"
    ),
)

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False)

    scanner_id: Mapped[int] = mapped_column(
        ForeignKey("scanners.id"),
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )