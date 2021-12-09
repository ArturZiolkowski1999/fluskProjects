from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'twoj_stary_pijany'


class NameForm(FlaskForm):
    name = StringField('Whats your name?', validators=[DataRequired()])
    submit = SubmitField("Send")


class PhotoForm(FlaskForm):
    # name = StringField("Name: ", validators=[DataRequired()])
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Send')


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
def form(name):
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

    return render_template('user.html', form=form, name=name)

@app.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404


app.run(debug=True)
