from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.db import db_mode_label, session_scope
from app.services import maintenance_service, oil_service
from app.services.seed import seed_if_empty

bp = Blueprint("dashboard", __name__)


@bp.get("/")
def index():
    with session_scope() as session:
        seed_if_empty(session)
        settings = oil_service.get_or_create_settings(session)
        oil = oil_service.compute_oil_reminder(settings)
        records = maintenance_service.list_records(session)
        summary = maintenance_service.totals(records)
        upcoming = [
            r
            for r in records
            if r.next_change_date is not None
        ][:5]
        upcoming.sort(key=lambda r: r.next_change_date)
        if oil.overdue:
            oil_progress = 100.0
        else:
            used = max(0, oil.current_odometer - oil.last_oil_change_km)
            oil_progress = min(100.0, (used / oil.interval_km) * 100.0)
        return render_template(
            "index.html",
            oil=oil,
            oil_progress=oil_progress,
            records=records[:8],
            summary=summary,
            upcoming=upcoming,
            db_mode=db_mode_label(),
        )


@bp.post("/odometro")
def update_odometer():
    with session_scope() as session:
        oil_service.update_odometer(
            session,
            current_odometer=request.form.get("current_odometer", 0),
            last_oil_change_km=request.form.get("last_oil_change_km", 0),
            vehicle_label=request.form.get("vehicle_label", "Mi vehículo"),
        )
    flash("Odómetro y recordatorio de aceite actualizados.", "success")
    return redirect(url_for("dashboard.index"))
