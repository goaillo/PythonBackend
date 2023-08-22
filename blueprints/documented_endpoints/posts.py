import base64
import datetime
from flask import Blueprint, request, abort
from blueprints.models.image_file import PostImageFile
from blueprints.models.post import Post
from blueprints.models.user import User
from blueprints.models import db
blueprint = Blueprint('post', __name__)

def serialize_post(post):
    # render_pic = base64.b64encode(data).decode('ascii') 
    # return render_pic
    return {
        "post_id": post.id,
        "post_name": post.name,
        "start_date": post.start_date,
        "end_date": post.end_date,
        "image": post.image
    }

@blueprint.get('/post')
def return_post():
    user_id = request.args.get('user_id', None)
    posts = Post.query.filter_by(user_id=user_id).all()
    if len(posts) > 0:
        return[serialize_post(post) for post in posts] 
    else:
        abort(404)

@blueprint.get('/post/<int:post_id>')
def return_specific_post(post_id):
    # show the post with the given id, the id is an integer

    post = Post.query.get(post_id)
    if post is not None:
        return serialize_post(post)
    else:
        abort(404)

def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic


@blueprint.post('/post')
def create_post():
    post = Post(
        name=request.form['name'],
        start_date=datetime.datetime.fromisoformat(request.form['start_date']),
        end_date=(datetime.datetime.fromisoformat(request.form['end_date']) if 'end_date' in request.form else None),
        user_id=User.query.get(request.form['user_id']).id
    )

    if 'inputFile' in request.files:
        file = request.files['inputFile']
        data = file.read()
        render_file = render_picture(data)

        newFile = PostImageFile(name=file.filename, data=data, 
        rendered_data=render_file)
        
        post.image = newFile

    db.session.add(post)
    db.session.commit()

    return serialize_post(post)
