import os
from app import create_app, db

# 1. Create the app instance first
app = create_app(os.environ.get("FLASK_ENV", "development"))

# 2. Use the created app instance to build the database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8000)
