from app.controllers.dashboard import bp as dashboard_bp
from app.controllers.maintenance import bp as maintenance_bp
from app.controllers.oil import bp as oil_bp


def register_blueprints(app):
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(maintenance_bp)
    app.register_blueprint(oil_bp)
