import os

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

from app import create_app
from app.extensions import db

app = create_app(os.environ.get("FLASK_ENV", "development"))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=False, host="0.0.0.0", port=port)
        