from flask import render_template, redirect, url_for, request, flash
from . import auth
from .. import main
from .forms import LoginForm
from ..models.models import User
from flask_login import login_user, logout_user, login_required


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(form.email.data)
        print(User.query.filter_by(email="aaartiii99@gmail.com").first())
        print(user)
        print(str(form.email.data) == "aaartiii99@gmail.com")
        if user is not None and user.verify_password(form.password.data):
            print("zalogowany")
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswth('/'):
                next = url_for('main.index')
            return redirect(url_for('main.index'))
        flash('Incorrect password or user name')
    return render_template(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You has been logged out')
    return redirect(url_for('main.index'))
