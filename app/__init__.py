import cloudinary

from flask import Flask

from config import config
from app.extensions import db, migrate, csrf
from app.routes import main_bp, notices_bp, gallery_bp, contact_bp
from app.routes.admin import admin_bp


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config["default"]))

    if app.config.get("CLOUDINARY_URL"):
        cloudinary.config(
            cloudinary_url=app.config.get("CLOUDINARY_URL"),
            secure=True,
        )
    else:
        cloudinary.config(
            cloud_name=app.config.get("CLOUDINARY_CLOUD_NAME"),
            api_key=app.config.get("CLOUDINARY_API_KEY"),
            api_secret=app.config.get("CLOUDINARY_API_SECRET"),
            secure=True,
        )

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(notices_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_globals():
        from datetime import datetime
        now = datetime.now()
        return {"current_year": now.year, "now": now}

    return app
