from flask import Blueprint
blueprint = Blueprint('post', __name__)

def serialize_post(post_id):
    return {
        "post_id": post_id,
        "post": 'post'
    }

@blueprint.get('/post/<int:post_id>')
def return_post(post_id):
    # show the post with the given id, the id is an integer
    return serialize_post(post_id)


@blueprint.post('/post')
def create_post():
    # show the post with the given id, the id is an integer
    # TODO Create a real post
    return serialize_post(post_id=1)

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('profile', username='John Doe'))
