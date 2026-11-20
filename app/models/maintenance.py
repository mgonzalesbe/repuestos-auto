from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    part_type: Mapped[str] = mapped_column(String(200), nullable=False)
    parts_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    labor_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    is_original: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    next_change_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    odometer_km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    @property
    def total_price(self) -> Decimal:
        return (self.parts_price or Decimal("0")) + (self.labor_price or Decimal("0"))
