from flask import render_template, redirect, url_for, request, flash
from . import auth
from .forms import LoginForm
from ..models.models import User
from flask_login import login_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswth('/'):
                next = url_for('main.index')
        return redirect(url_for(next))
    flash('Incorrect password or user name')
    return render_template('auth/login.html', form=form)
