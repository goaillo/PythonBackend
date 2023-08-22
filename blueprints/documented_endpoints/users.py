from flask import Blueprint, request, abort
from sqlalchemy import delete
from blueprints.models.user import User
from blueprints.models import db
blueprint = Blueprint('user', __name__)

def serialize_user(user:User):
    return {
        "user_id": user.id,
        "user_name": user.username,
        "email": user.email
    }

@blueprint.get('/user/<int:user_id>')
def return_user(user_id):
    # show the user with the given id, the id is an integer
    user = User.query.get(user_id)
    if user is not None:
        return serialize_user(user)
    else:
        abort(404)


@blueprint.post('/user')
def create_user():
    user = User(
        username=request.form['username'],
        email=request.form['email'],
    )
    db.session.add(user)
    db.session.commit()
    return serialize_user(user)

@blueprint.delete('/user/<int:user_id>')
def delete_user(user_id):
    db.session.execute(delete(User).where(User.id == user_id))
    db.session.commit()
    return "Deleted"

