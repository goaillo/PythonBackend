from flask import Blueprint, abort, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash

from blueprints.models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    if not user or not check_password_hash(user.password, password):
        abort(400, "Bad Credentials")

    login_user(user, remember=remember)
    return "Logged"


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logout"
