from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.maintenance import MaintenanceRecord
from app.models.vehicle import VehicleSettings
from app.services.oil_service import get_or_create_settings


def seed_if_empty(session: Session) -> bool:
    """Insert sample data so the empty UI is understandable. Returns True if seeded."""
    settings = get_or_create_settings(session)
    has_records = session.query(MaintenanceRecord).count() > 0
    if has_records and settings.current_odometer > 0:
        return False

    today = date.today()
    if settings.current_odometer == 0 and settings.last_oil_change_km == 0:
        settings.current_odometer = 84520
        settings.last_oil_change_km = 79800
        settings.vehicle_label = "Toyota Corolla 2019"

    if not has_records:
        samples = [
            MaintenanceRecord(
                service_date=today - timedelta(days=120),
                part_type="Cambio de aceite y filtro",
                parts_price=Decimal("48.50"),
                labor_price=Decimal("35.00"),
                is_original=True,
                next_change_date=today + timedelta(days=60),
                odometer_km=79800,
                notes="Aceite sintético 5W-30. Intervalo 7.000 km.",
            ),
            MaintenanceRecord(
                service_date=today - timedelta(days=45),
                part_type="Pastillas de freno delanteras",
                parts_price=Decimal("92.00"),
                labor_price=Decimal("60.00"),
                is_original=False,
                next_change_date=today + timedelta(days=300),
                odometer_km=83200,
                notes="Marca aftermarket certificada.",
            ),
            MaintenanceRecord(
                service_date=today - timedelta(days=10),
                part_type="Filtro de aire",
                parts_price=Decimal("22.00"),
                labor_price=Decimal("15.00"),
                is_original=True,
                next_change_date=today + timedelta(days=200),
                odometer_km=84200,
                notes=None,
            ),
        ]
        session.add_all(samples)
    session.flush()
    return True
