from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField("Phone", validators=[Optional(), Length(max=20)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField("Send Message")


class AdmissionForm(FlaskForm):
    name = StringField("Student Name", validators=[DataRequired(), Length(max=100)])
    email = StringField("Parent Email", validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField("Phone", validators=[DataRequired(), Length(max=20)])
    message = TextAreaField(
        "Additional Details",
        validators=[Optional(), Length(max=2000)],
        description="Grade applying for, any special requirements, etc.",
    )
    submit = SubmitField("Submit Inquiry")
