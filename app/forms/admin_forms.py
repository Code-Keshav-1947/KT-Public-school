from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, DateTimeLocalField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Optional


class AdminLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=100)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class NoticeForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    body = TextAreaField("Body", validators=[DataRequired()], render_kw={"rows": 10})
    published_at = DateTimeLocalField(
        "Publish Date",
        validators=[Optional()],
        format="%Y-%m-%dT%H:%M",
    )
    is_published = BooleanField("Published", default=True)
    submit = SubmitField("Save Notice")


class GalleryForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    image_path = StringField(
        "Image Path",
        validators=[DataRequired(), Length(max=500)],
        description="Path under static/, e.g. img/gallery/sports_day.svg",
    )
    caption = StringField("Caption", validators=[Optional(), Length(max=500)])
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save Image")
