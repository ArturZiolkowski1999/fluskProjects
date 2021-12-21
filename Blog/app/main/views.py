from flask import render_template, redirect, url_for, request, flash
import os
from flasky import db
from werkzeug import secure_filename
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PictureForm
from ..models.models import User, Role
from flask_login import login_user, logout_user, login_required, current_user
from ..models.decorators import admin_required
from ..models.photos import photos


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


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        os.rename(('/home/ziolko/fluskProjects/Blog/app/static/' + current_user.username),
                  ('/home/ziolko/fluskProjects/Blog/app/static/' + form.username.data))
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('Profile has been actualized')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/upload-picture', methods=['GET', 'POST'])
@login_required
def upload_picture():
    form = PictureForm()
    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save('/home/ziolko/fluskProjects/Blog/app/static/' + current_user.username + '/' + filename)
        flash('photo has been sent')
        return redirect(url_for('.user', username=current_user.username))
    return render_template('upload_picture.html', form=form)
