from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, BooleanField, StringField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 64),
                                              Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember_me')
    submit = SubmitField('Login')

