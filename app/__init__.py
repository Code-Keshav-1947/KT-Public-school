from flask import Flask

from config import config
from app.extensions import db, migrate, csrf
from app.routes import main_bp, notices_bp, gallery_bp, contact_bp


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(notices_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(contact_bp)

    @app.context_processor
    def inject_globals():
        from datetime import datetime
        return {"current_year": datetime.now().year}

    return app
