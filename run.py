import os
from app import create_app, db

# 1. Create the app instance first
app = create_app(os.environ.get("FLASK_ENV", "development"))

# 2. Use the created app instance to build the database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # यह लाइन रेंडर के पोर्ट को अपने आप पहचान लेगी
    port = int(os.environ.get("PORT", 8000))
    # host को '0.0.0.0' रखने से यह इंटरनेट पर लाइव होने के लिए तैयार हो जाता है
    app.run(debug=False, host='0.0.0.0', port=port)
