from flask import render_template, redirect, url_for, request, flash
from flasky import db
from . import main
from .forms import EditProfileForm
from ..models.models import User
from flask_login import login_user, logout_user, login_required, current_user


@main.route("/")
def index():
    return render_template('index.html')


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', 404)


@main.errorhandler(403)
def permission_denied(e):
    return render_template('403.html', 403)


@main.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', 500)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('your account has ben actualized')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

