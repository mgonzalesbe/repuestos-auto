from flask import Blueprint, redirect, url_for

bp = Blueprint("oil", __name__, url_prefix="/aceite")


@bp.get("/")
def oil_page():
    """Oil reminder lives on the dashboard; keep a friendly alias route."""
    return redirect(url_for("dashboard.index") + "#aceite")
