from flask import render_template, redirect, url_for, request, flash
from . import main
from ..models.models import User
from flask_login import login_user, logout_user, login_required


@main.route("/")
def index():
    return render_template('index.html')
