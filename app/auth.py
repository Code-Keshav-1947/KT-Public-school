import secrets
from functools import wraps

from flask import current_app, redirect, session, url_for


def verify_admin(username: str, password: str) -> bool:
    expected_user = current_app.config["ADMIN_USERNAME"]
    expected_pass = current_app.config["ADMIN_PASSWORD"]
    return secrets.compare_digest(username, expected_user) and secrets.compare_digest(
        password, expected_pass
    )


def login_admin():
    session["admin_logged_in"] = True
    session.permanent = True


def logout_admin():
    session.pop("admin_logged_in", None)


def is_admin_logged_in() -> bool:
    return session.get("admin_logged_in") is True


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not is_admin_logged_in():
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)

    return wrapped
