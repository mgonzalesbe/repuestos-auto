#!/usr/bin/env python3
"""One-shot wipe of demo / sample rows. Does not drop schema or migrations.

Requires CONFIRM=YES so it cannot run by accident (e.g. on deploy).

Usage (local SQLite or any DATABASE_URL):
  CONFIRM=YES python scripts/clear_demo_data.py

On Render (if Shell is available on the web service):
  CONFIRM=YES python scripts/clear_demo_data.py

If you cannot reach the DB from here, run the SQL in
scripts/clear_demo_data.sql via the Render Postgres dashboard instead.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqlalchemy import text  # noqa: E402

from app.db import get_engine, init_db  # noqa: E402


def main() -> int:
    if os.environ.get("CONFIRM", "").strip().upper() != "YES":
        print(
            "Refusing to run: set CONFIRM=YES to delete all maintenance_records "
            "and reset vehicle_settings.",
            file=sys.stderr,
        )
        return 2

    init_db()
    engine = get_engine()
    with engine.begin() as conn:
        deleted = conn.execute(text("DELETE FROM maintenance_records")).rowcount
        # Reset any settings rows to empty defaults (keep row so UI still works).
        updated = conn.execute(
            text(
                "UPDATE vehicle_settings SET "
                "current_odometer = 0, "
                "last_oil_change_km = 0, "
                "vehicle_label = 'Mi vehículo'"
            )
        ).rowcount
        # SQLite has no TIMESTAMPTZ NOW() in a portable ORM-free way for updated_at;
        # app will refresh on next write. Postgres trigger not required.
    print(
        f"clear_demo_data: deleted {deleted} maintenance row(s), "
        f"reset {updated} vehicle_settings row(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
