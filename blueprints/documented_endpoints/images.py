from io import BytesIO

from flask import Blueprint, abort, request, send_file
from flask_login import current_user, login_required

from blueprints.models import db
from blueprints.models.image_file import PostImageFile
from blueprints.models.post import Post

blueprint = Blueprint("images", __name__)


@blueprint.get("/post-image/<int:post_image_id>")
@login_required
def return_post_image(post_image_id):
    # TODO Test if User can get this image
    post_image = PostImageFile.query.get(post_image_id)
    if not post_image:
        abort(404)

    with open(post_image.image_path, "rb") as f:
        return send_file(
            BytesIO(f.read()), mimetype="image/jpg", download_name=post_image.name
        )
