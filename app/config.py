import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SQLITE_PATH = BASE_DIR / "data" / "repuestos.db"
OIL_INTERVAL_KM = 7000


def database_url() -> str:
    """Return DATABASE_URL when set; otherwise a local SQLite file.

    Neon / Render often inject ``postgres://``; SQLAlchemy + psycopg3 need
    ``postgresql+psycopg://``. On Render (``RENDER=true``) SQLite fallback is
    refused so a missing env var fails loudly instead of using ephemeral disk.
    """
    url = (os.environ.get("DATABASE_URL") or "").strip()
    if url:
        # Neon / Render / common hosted Postgres often use postgres://
        if url.startswith("postgres://"):
            url = "postgresql+psycopg://" + url[len("postgres://") :]
        elif url.startswith("postgresql://") and "+psycopg" not in url:
            url = "postgresql+psycopg://" + url[len("postgresql://") :]
        return url
    if os.environ.get("RENDER"):
        raise RuntimeError(
            "DATABASE_URL is required on Render. Paste the Neon Postgres "
            "connection string in the web service Environment tab "
            "(prefer the pooled URI)."
        )
    SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{SQLITE_PATH}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "repuestos-auto-dev-key")
    SQLALCHEMY_DATABASE_URI = database_url()
    OIL_INTERVAL_KM = OIL_INTERVAL_KM
