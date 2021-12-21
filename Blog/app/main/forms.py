from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, ValidationError, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from ..models.models import User, Role
from ..models.photos import photos


class EditProfileForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(1, 64)])
    location = StringField('location', validators=[DataRequired(), Length(1, 64)])
    about_me = TextAreaField('about me')
    submit = SubmitField('edit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 64),
                                             Email(), ])

    username = StringField('username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'your name could contain only letters,'
                                                          ' digits, dots add_')])
    confirmed = BooleanField('confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('name', validators=[DataRequired(), Length(1, 64)])
    location = StringField('location', validators=[DataRequired(), Length(1, 64)])
    about_me = TextAreaField('about me')
    submit = SubmitField('edit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use')


class PictureForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Images only'), FileRequired("File is required")])
    submit = SubmitField('Upload')
