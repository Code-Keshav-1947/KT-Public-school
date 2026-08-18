from flask import Blueprint, render_template

from app.models import GalleryImage

gallery_bp = Blueprint("gallery", __name__, url_prefix="/gallery")


@gallery_bp.route("/")
def index():
    images = (
        GalleryImage.query.filter_by(is_active=True)
        .order_by(GalleryImage.uploaded_at.desc())
        .all()
    )
    return render_template("gallery/index.html", images=images)
