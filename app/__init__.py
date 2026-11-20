from flask import Flask

from app.config import Config
from app.controllers import register_blueprints
from app.db import init_db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db()
    register_blueprints(app)

    @app.context_processor
    def inject_globals():
        return {
            "brand": "RepuestosAuto",
            "oil_interval_km": Config.OIL_INTERVAL_KM,
        }

    return app
