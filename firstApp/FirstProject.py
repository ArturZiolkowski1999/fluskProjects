from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'twoj_stary_pijany'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# class BaseConfig(object):
#     DEBUG = True
#     TESTING = False
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'data.sqlite')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#


class NameForm(FlaskForm):
    name = StringField('Whats your name?', validators=[DataRequired()])
    submit = SubmitField("Send")


class PhotoForm(FlaskForm):
    # name = StringField("Name: ", validators=[DataRequired()])
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Send')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.route('/', methods=['GET', 'POST'])
def index():

    form = PhotoForm()

    if form.validate_on_submit():
        name = form.photo.data
        filename = secure_filename(name.filename)
        name.save(os.path.join(
            app.instance_path, 'photos', filename))

    return render_template('index.html', form=form)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.route('/form', methods=['GET', 'POST'])
def form():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('form'))

    return render_template('form.html', form=form,
                           name=session.get('name'),
                           known=session.get('known', False))


@app.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404


app.run(debug=True)
