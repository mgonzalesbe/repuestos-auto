from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.db import session_scope
from app.services import maintenance_service

bp = Blueprint("maintenance", __name__, url_prefix="/mantenimientos")


@bp.get("/")
def list_view():
    with session_scope() as session:
        records = maintenance_service.list_records(session)
        summary = maintenance_service.totals(records)
        return render_template(
            "maintenance_list.html",
            records=records,
            summary=summary,
        )


@bp.get("/nuevo")
def new_form():
    return render_template("maintenance_form.html", record=None, action="create")


@bp.post("/nuevo")
def create():
    with session_scope() as session:
        maintenance_service.create_record(session, request.form)
    flash("Registro de mantenimiento guardado.", "success")
    return redirect(url_for("maintenance.list_view"))


@bp.get("/<int:record_id>/editar")
def edit_form(record_id: int):
    with session_scope() as session:
        record = maintenance_service.get_record(session, record_id)
        if record is None:
            abort(404)
        return render_template(
            "maintenance_form.html",
            record=record,
            action="edit",
        )


@bp.post("/<int:record_id>/editar")
def update(record_id: int):
    with session_scope() as session:
        record = maintenance_service.get_record(session, record_id)
        if record is None:
            abort(404)
        maintenance_service.update_record(session, record, request.form)
    flash("Registro actualizado.", "success")
    return redirect(url_for("maintenance.list_view"))


@bp.post("/<int:record_id>/eliminar")
def delete(record_id: int):
    with session_scope() as session:
        record = maintenance_service.get_record(session, record_id)
        if record is None:
            abort(404)
        maintenance_service.delete_record(session, record)
    flash("Registro eliminado.", "success")
    return redirect(url_for("maintenance.list_view"))
