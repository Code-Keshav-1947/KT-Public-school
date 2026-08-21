import cloudinary.uploader

from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request

from app.auth import admin_required, is_admin_logged_in, login_admin, logout_admin, verify_admin
from app.extensions import db
from app.forms.admin_forms import AdminLoginForm, NoticeForm, GalleryForm
from app.models import Notice, GalleryImage, Inquiry

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _upload_to_cloudinary(file):
    return cloudinary.uploader.upload(
        file,
        folder="kt_public_school/gallery",
        resource_type="image",
    )


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if is_admin_logged_in():
        return redirect(url_for("admin.dashboard"))

    form = AdminLoginForm()
    if form.validate_on_submit():
        if verify_admin(form.username.data, form.password.data):
            login_admin()
            flash("Welcome back!", "success")
            next_url = request.args.get("next")
            if next_url:
                return redirect(next_url)
            return redirect(url_for("admin.dashboard"))
        flash("Invalid username or password.", "danger")

    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout")
@admin_required
def logout():
    logout_admin()
    flash("You have been signed out.", "info")
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@admin_required
def dashboard():
    stats = {
        "notices": Notice.query.count(),
        "published_notices": Notice.query.filter_by(is_published=True).count(),
        "gallery": GalleryImage.query.count(),
        "inquiries": Inquiry.query.count(),
    }
    recent_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).limit(5).all()
    return render_template("admin/dashboard.html", stats=stats, inquiries=recent_inquiries)


# --- Notices ---

@admin_bp.route("/notices")
@admin_required
def notices_list():
    notices = Notice.query.order_by(Notice.published_at.desc()).all()
    return render_template("admin/notices/list.html", notices=notices)


@admin_bp.route("/notices/new", methods=["GET", "POST"])
@admin_required
def notice_create():
    form = NoticeForm()
    if form.validate_on_submit():
        notice = Notice(
            title=form.title.data,
            body=form.body.data,
            published_at=form.published_at.data or datetime.utcnow(),
            is_published=form.is_published.data,
        )
        db.session.add(notice)
        db.session.commit()
        flash("Notice created successfully.", "success")
        return redirect(url_for("admin.notices_list"))
    if request.method == "GET" and not form.published_at.data:
        form.published_at.data = datetime.utcnow()
    return render_template("admin/notices/form.html", form=form, title="New Notice")


@admin_bp.route("/notices/<int:notice_id>/edit", methods=["GET", "POST"])
@admin_required
def notice_edit(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    form = NoticeForm(obj=notice)
    if form.validate_on_submit():
        notice.title = form.title.data
        notice.body = form.body.data
        notice.published_at = form.published_at.data or datetime.utcnow()
        notice.is_published = form.is_published.data
        db.session.commit()
        flash("Notice updated successfully.", "success")
        return redirect(url_for("admin.notices_list"))
    return render_template("admin/notices/form.html", form=form, title="Edit Notice", notice=notice)


@admin_bp.route("/notices/<int:notice_id>/delete", methods=["POST"])
@admin_required
def notice_delete(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    db.session.delete(notice)
    db.session.commit()
    flash("Notice deleted.", "info")
    return redirect(url_for("admin.notices_list"))


# --- Gallery ---

@admin_bp.route("/gallery")
@admin_required
def gallery_list():
    images = GalleryImage.query.order_by(GalleryImage.uploaded_at.desc()).all()
    return render_template("admin/gallery/list.html", images=images)


# --- Gallery ---

@admin_bp.route("/gallery/new", methods=["GET", "POST"])
@admin_required
def gallery_create():
    form = GalleryForm()
    if form.validate_on_submit():
        file_to_upload = request.files.get(form.image_path.name)

        if not file_to_upload or not file_to_upload.filename:
            flash("Please select an image to upload.", "danger")
            return render_template("admin/gallery/form.html", form=form, title="Add Gallery Image")

        try:
            upload_result = _upload_to_cloudinary(file_to_upload)
            final_image_url = upload_result["secure_url"]
        except Exception as e:
            flash(f"Cloudinary upload error: {e}", "danger")
            return render_template("admin/gallery/form.html", form=form, title="Add Gallery Image")

        image = GalleryImage(
            title=form.title.data,
            image_path=final_image_url,
            caption=form.caption.data or None,
            is_active=form.is_active.data,
        )
        db.session.add(image)
        db.session.commit()
        flash("Gallery image added successfully.", "success")
        return redirect(url_for("admin.gallery_list"))

    return render_template("admin/gallery/form.html", form=form, title="Add Gallery Image")



@admin_bp.route("/gallery/<int:image_id>/edit", methods=["GET", "POST"])
@admin_required
def gallery_edit(image_id):
    image = GalleryImage.query.get_or_404(image_id)
    form = GalleryForm(obj=image)
    if form.validate_on_submit():
        file_to_upload = request.files.get(form.image_path.name)
        final_image_url = image.image_path

        if file_to_upload and file_to_upload.filename:
            try:
                upload_result = _upload_to_cloudinary(file_to_upload)
                final_image_url = upload_result["secure_url"]
            except Exception as e:
                flash(f"Cloudinary upload error: {e}", "danger")
                return render_template(
                    "admin/gallery/form.html",
                    form=form,
                    title="Edit Gallery Image",
                    image=image,
                )

        image.title = form.title.data
        image.image_path = final_image_url
        image.caption = form.caption.data or None
        image.is_active = form.is_active.data
        db.session.commit()
        flash("Gallery image updated successfully.", "success")
        return redirect(url_for("admin.gallery_list"))
    return render_template("admin/gallery/form.html", form=form, title="Edit Gallery Image", image=image)


@admin_bp.route("/gallery/<int:image_id>/delete", methods=["POST"])
@admin_required
def gallery_delete(image_id):
    image = GalleryImage.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    flash("Gallery image deleted.", "info")
    return redirect(url_for("admin.gallery_list"))


# --- Inquiries (read-only) ---

@admin_bp.route("/inquiries")
@admin_required
def inquiries_list():
    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    return render_template("admin/inquiries/list.html", inquiries=inquiries)
