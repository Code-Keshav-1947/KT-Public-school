import os

from app import create_app
from app.extensions import db

app = create_app(os.environ.get("FLASK_ENV", "development"))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=False, host="0.0.0.0", port=port)
