from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Scanner(Base):
    __tablename__ = "scanners"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    serial_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    branch_id: Mapped[int] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False
    )