import datetime
import logging
import os
import time

from flask import Blueprint, abort, request
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
    }


@blueprint.get("/post")
def return_post():
    user_id = request.args.get("user_id", None)
    posts = Post.query.filter_by(user_id=user_id).all()
    if len(posts) > 0:
        return [serialize_post(post) for post in posts]
    else:
        abort(404)


@blueprint.get("/post/<int:post_id>")
def return_specific_post(post_id):
    # show the post with the given id, the id is an integer

    post = Post.query.get(post_id)
    if post is not None:
        return serialize_post(post)
    else:
        abort(404)


@blueprint.post("/post")
def create_post():
    post = Post(
        name=request.form["name"],
        start_date=datetime.datetime.fromisoformat(request.form["start_date"]),
        end_date=(
            datetime.datetime.fromisoformat(request.form["end_date"])
            if "end_date" in request.form
            else None
        ),
        user_id=User.query.get(request.form["user_id"]).id,
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
        tmp_path = os.path.join(Config.uploadFolder, filename_tmp)
        file.save(tmp_path)

        try:
            image_to_resize = Image.open(tmp_path)
            width, height = image_to_resize.size
            new_size = (width // 2, height // 2)
            resized_image = image_to_resize.resize(new_size)
            resized_name = "compressed_image_{}{}".format(
                int(time.time()), os.path.splitext(filename_uploaded)[1]
            )
            resized_image_path = os.path.join(Config.filesFolder, resized_name)
            resized_image.save(resized_image_path, optimize=True, quality=50)

            db.session.add(
                PostImageFile(name=filename_uploaded, image_path=resized_image_path)
            )
            post.image_path = resized_image_path

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
