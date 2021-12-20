from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, BooleanField, StringField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models.models import User

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 64),
                                              Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember_me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 64),
                                         Email()])

    username = StringField('username', validators=[DataRequired(),  Length(1,64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'your name could contain only letters,'
                                                          ' digits, dots add_')])
    password = PasswordField('password', validators=[DataRequired(),
                                                     EqualTo('password2', message='passwords has to be the same')])
    password2 = PasswordField('verify your password', validators=[DataRequired()])
    submit = SubmitField('register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email has been already used')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('This username has been already used')
