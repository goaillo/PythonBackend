from flask import Blueprint, abort, request
from flask_login import current_user, login_required
from sqlalchemy import delete
from werkzeug.security import generate_password_hash

from blueprints.models import db
from blueprints.models.user import User
from tools.wrapper import isAdmin

blueprint = Blueprint("user", __name__)


def serialize_user(user: User):
    return {"user_id": user.id, "user_name": user.username, "email": user.email}


@blueprint.get("/user/<int:user_id>")
@login_required
def return_user(user_id):
    # show the user with the given id, the id is an integer
    user = User.query.get(user_id)
    if user is not None:
        return serialize_user(user)
    else:
        abort(404)


@blueprint.post("/user")
def create_user():
    user = User.query.filter_by(email=request.form["email"]).first()
    if user:
        abort(400, "Email already taken")

    user = User(
        username=request.form["username"],
        email=request.form["email"],
        password=generate_password_hash(request.form["password"], method="scrypt"),
    )
    db.session.add(user)
    db.session.commit()
    return serialize_user(user)


@blueprint.delete("/user/<int:user_id>")
@isAdmin
def delete_user(user_id):
    db.session.execute(
        delete(User).where(User.is_admin == False).where(User.id == user_id)
    )
    db.session.commit()

    return {}
