from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class VehicleSettings(Base):
    __tablename__ = "vehicle_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    current_odometer: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_oil_change_km: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    vehicle_label: Mapped[str] = mapped_column(String(120), nullable=False, default="Mi vehículo")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
