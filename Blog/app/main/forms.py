from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models.models import User


class EditProfileForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(1, 64)])
    location = StringField('location', validators=[DataRequired(), Length(1, 64)])
    about_me = TextAreaField('about me')
    submit = SubmitField('edit')
