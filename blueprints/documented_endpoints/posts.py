import datetime
import logging
import os
import time

from flask import Blueprint, abort, redirect, request, url_for
from flask_login import current_user, login_required
from PIL import Image

from blueprints.models import db
from blueprints.models.image_file import PostImageFile
from blueprints.models.post import Post
from blueprints.models.user import User
from config import Config

blueprint = Blueprint("post", __name__)


def serialize_post(post):
    return {
        "post_id": post.id,
        "post_name": post.name,
        "start_date": post.start_date,
        "end_date": post.end_date,
        "image_path": post.image_path,
    }


@blueprint.get("/post")
@login_required
def return_post():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    if len(posts) > 0:
        return [serialize_post(post) for post in posts]
    else:
        abort(404)


@blueprint.get("/post/<int:post_id>")
@login_required
def return_specific_post(post_id):
    # show the post with the given id if it's the right user
    post = Post.query.filter_by(user_id=current_user.id, id=post_id)
    if post is not None:
        return serialize_post(post)
    else:
        abort(404)


@blueprint.post("/post")
@login_required
def create_post():
    post = Post(
        name=request.form["name"],
        start_date=datetime.datetime.fromisoformat(request.form["start_date"]),
        end_date=(
            datetime.datetime.fromisoformat(request.form["end_date"])
            if "end_date" in request.form
            else None
        ),
        user_id=current_user.id,
    )

    if "inputFile" in request.files:
        file = request.files["inputFile"]

        # Download uploaded file to the system to compress it
        filename_uploaded = file.filename
        filename_tmp = "{}_{}{}".format(
            os.path.splitext(filename_uploaded)[0],
            int(time.time()),
            os.path.splitext(filename_uploaded)[1],
        )
        tmp_path = os.path.join(Config.TMP_FOLDER, filename_tmp)
        file.save(tmp_path)

        try:
            image_to_resize = Image.open(tmp_path)
            width, height = image_to_resize.size
            new_size = (width // 2, height // 2)
            resized_image = image_to_resize.resize(new_size)
            resized_name = "compressed_image_{}{}".format(
                int(time.time()), os.path.splitext(filename_uploaded)[1]
            )
            resized_image_path = os.path.join(Config.FILES_FOLDER, resized_name)
            resized_image.save(resized_image_path, optimize=True, quality=50)

            post_image = PostImageFile(
                name=filename_uploaded, image_path=resized_image_path
            )
            db.session.add(post_image)
            db.session.commit()
            post.image_path = url_for(
                "images.return_post_image", post_image_id=post_image.id
            )

            # Remove tmp files
            os.remove(tmp_path)
        except Exception as e:
            # Delete tmp images if something is wrong
            logging.error(e)
            logging.info(filename_uploaded, post.user_id)
            os.remove(tmp_path)
            os.remove(resized_image_path)

    db.session.add(post)
    db.session.commit()

    return serialize_post(post)
