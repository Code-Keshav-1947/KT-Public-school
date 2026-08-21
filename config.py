import os

from dotenv import load_dotenv

load_dotenv()

# Clean CLOUDINARY_URL if present to avoid Cloudinary SDK initialization crash
_c_url = os.environ.get("CLOUDINARY_URL", "").strip().strip("\"'")
if _c_url:
    if not _c_url.startswith("cloudinary://"):
        if "@" in _c_url and ":" in _c_url:
            os.environ["CLOUDINARY_URL"] = f"cloudinary://{_c_url}"
        else:
            os.environ.pop("CLOUDINARY_URL", None)
    else:
        os.environ["CLOUDINARY_URL"] = _c_url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    db_url = os.environ.get("DATABASE_URL", "sqlite:///kt_public_school.db")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = db_url
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
    CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL")
    CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
