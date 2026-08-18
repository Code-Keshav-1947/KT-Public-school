import os

from app import create_app, db 

with create_app.app_context():
    db.create_all()


app = create_app(os.environ.get("FLASK_ENV", "development"))

if __name__ == "__main__":
    app.run(debug=True)
