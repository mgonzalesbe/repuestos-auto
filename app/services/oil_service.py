from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.config import OIL_INTERVAL_KM
from app.models.vehicle import VehicleSettings


@dataclass
class OilReminder:
    current_odometer: int
    last_oil_change_km: int
    interval_km: int
    due_at_km: int
    remaining_km: int
    overdue: bool
    vehicle_label: str

    @property
    def status_label(self) -> str:
        if self.overdue:
            return "Vencido"
        if self.remaining_km <= 500:
            return "Próximo"
        return "Al día"


def get_or_create_settings(session: Session) -> VehicleSettings:
    settings = session.query(VehicleSettings).order_by(VehicleSettings.id.asc()).first()
    if settings is None:
        settings = VehicleSettings(
            current_odometer=0,
            last_oil_change_km=0,
            vehicle_label="Mi vehículo",
        )
        session.add(settings)
        session.flush()
    return settings


def compute_oil_reminder(settings: VehicleSettings) -> OilReminder:
    due_at = settings.last_oil_change_km + OIL_INTERVAL_KM
    remaining = due_at - settings.current_odometer
    return OilReminder(
        current_odometer=settings.current_odometer,
        last_oil_change_km=settings.last_oil_change_km,
        interval_km=OIL_INTERVAL_KM,
        due_at_km=due_at,
        remaining_km=remaining,
        overdue=remaining <= 0,
        vehicle_label=settings.vehicle_label or "Mi vehículo",
    )


def update_odometer(
    session: Session,
    *,
    current_odometer: int,
    last_oil_change_km: int,
    vehicle_label: str,
) -> OilReminder:
    settings = get_or_create_settings(session)
    settings.current_odometer = max(0, int(current_odometer))
    settings.last_oil_change_km = max(0, int(last_oil_change_km))
    settings.vehicle_label = (vehicle_label or "Mi vehículo").strip()[:120]
    session.flush()
    return compute_oil_reminder(settings)
