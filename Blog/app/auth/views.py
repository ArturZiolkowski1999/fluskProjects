from flask import render_template, redirect, url_for
from . import auth
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)
