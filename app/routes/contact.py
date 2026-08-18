from flask import Blueprint, render_template, flash, redirect, url_for

from app.extensions import db
from app.forms.inquiry_forms import ContactForm, AdmissionForm
from app.models import Inquiry

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        inquiry = Inquiry(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            message=form.message.data,
            inquiry_type="contact",
        )
        db.session.add(inquiry)
        db.session.commit()
        flash("Thank you! Your message has been sent successfully.", "success")
        return redirect(url_for("contact.contact"))
    return render_template("contact.html", form=form)


@contact_bp.route("/admissions/submit", methods=["POST"])
def admission_submit():
    form = AdmissionForm()
    if form.validate_on_submit():
        inquiry = Inquiry(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            message=form.message.data or "",
            inquiry_type="admission",
        )
        db.session.add(inquiry)
        db.session.commit()
        flash("Thank you! Your admission inquiry has been submitted.", "success")
        return redirect(url_for("main.admissions"))
    flash("Please correct the errors in the form.", "danger")
    return redirect(url_for("main.admissions"))
