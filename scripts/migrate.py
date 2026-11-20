#!/usr/bin/env python3
"""Apply SQL migrations when DATABASE_URL points at Postgres. No-op for SQLite."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import database_url  # noqa: E402
from app.db import get_engine, init_db  # noqa: E402
from sqlalchemy import text  # noqa: E402


def main() -> int:
    url = database_url()
    if url.startswith("sqlite"):
        print("migrate: using SQLite — applying ORM create_all")
        init_db()
        print("migrate: done")
        return 0

    migrations_dir = ROOT / "migrations"
    files = sorted(p for p in migrations_dir.glob("*.sql"))
    if not files:
        print("migrate: nothing to do")
        return 0

    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                "CREATE TABLE IF NOT EXISTS schema_migrations ("
                "name TEXT PRIMARY KEY, "
                "applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW())"
            )
        )
        done = {
            row[0]
            for row in conn.execute(text("SELECT name FROM schema_migrations")).fetchall()
        }
        for path in files:
            if path.name in done:
                continue
            sql = path.read_text(encoding="utf-8")
            conn.execute(text(sql))
            conn.execute(
                text("INSERT INTO schema_migrations (name) VALUES (:name)"),
                {"name": path.name},
            )
            print(f"migrate: applied {path.name}")
    print("migrate: done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
