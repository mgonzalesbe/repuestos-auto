from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation

from sqlalchemy.orm import Session

from app.models.maintenance import MaintenanceRecord


def list_records(session: Session) -> list[MaintenanceRecord]:
    return (
        session.query(MaintenanceRecord)
        .order_by(MaintenanceRecord.service_date.desc(), MaintenanceRecord.id.desc())
        .all()
    )


def get_record(session: Session, record_id: int) -> MaintenanceRecord | None:
    return session.get(MaintenanceRecord, record_id)


def _parse_money(value) -> Decimal:
    try:
        return Decimal(str(value or "0").replace(",", ".")).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return Decimal("0.00")


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def create_record(session: Session, data: dict) -> MaintenanceRecord:
    record = MaintenanceRecord(
        service_date=_parse_date(data.get("service_date")) or date.today(),
        part_type=(data.get("part_type") or "").strip()[:200] or "Mantenimiento",
        parts_price=_parse_money(data.get("parts_price")),
        labor_price=_parse_money(data.get("labor_price")),
        is_original=str(data.get("is_original", "1")) in {"1", "true", "yes", "on", "si", "sí"},
        next_change_date=_parse_date(data.get("next_change_date")),
        odometer_km=_optional_int(data.get("odometer_km")),
        notes=(data.get("notes") or "").strip() or None,
    )
    session.add(record)
    session.flush()
    return record


def update_record(session: Session, record: MaintenanceRecord, data: dict) -> MaintenanceRecord:
    record.service_date = _parse_date(data.get("service_date")) or record.service_date
    record.part_type = (data.get("part_type") or "").strip()[:200] or record.part_type
    record.parts_price = _parse_money(data.get("parts_price"))
    record.labor_price = _parse_money(data.get("labor_price"))
    record.is_original = str(data.get("is_original", "0")) in {"1", "true", "yes", "on", "si", "sí"}
    record.next_change_date = _parse_date(data.get("next_change_date"))
    record.odometer_km = _optional_int(data.get("odometer_km"))
    record.notes = (data.get("notes") or "").strip() or None
    record.updated_at = datetime.now(timezone.utc)
    session.flush()
    return record


def delete_record(session: Session, record: MaintenanceRecord) -> None:
    session.delete(record)
    session.flush()


def _optional_int(value) -> int | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def totals(records: list[MaintenanceRecord]) -> dict:
    parts = sum((r.parts_price or Decimal("0")) for r in records)
    labor = sum((r.labor_price or Decimal("0")) for r in records)
    return {
        "parts": parts,
        "labor": labor,
        "total": parts + labor,
        "count": len(records),
    }
