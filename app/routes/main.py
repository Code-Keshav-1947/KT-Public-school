from flask import Blueprint, render_template

from app.forms.inquiry_forms import AdmissionForm
from app.models import Notice

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    latest_notices = (
        Notice.query.filter_by(is_published=True)
        .order_by(Notice.published_at.desc())
        .limit(3)
        .all()
    )
    return render_template("home.html", notices=latest_notices)


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/admissions")
def admissions():
    form = AdmissionForm()
    return render_template("admissions.html", form=form)
