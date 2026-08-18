from flask import Blueprint, render_template, abort

from app.models import Notice

notices_bp = Blueprint("notices", __name__, url_prefix="/notices")


@notices_bp.route("/")
def list_notices():
    notices = (
        Notice.query.filter_by(is_published=True)
        .order_by(Notice.published_at.desc())
        .all()
    )
    return render_template("notices/list.html", notices=notices)


@notices_bp.route("/<int:notice_id>")
def notice_detail(notice_id):
    notice = Notice.query.filter_by(id=notice_id, is_published=True).first_or_404()
    return render_template("notices/detail.html", notice=notice)
