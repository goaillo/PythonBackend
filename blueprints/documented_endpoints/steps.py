import datetime
import logging
import os
import time

from flask import Blueprint, abort, request, url_for
from flask_login import current_user, login_required
from PIL import Image

from blueprints.documented_endpoints.posts import deserialize_post
from blueprints.models import db
from blueprints.models.image_file import ImageFile
from blueprints.models.post import Post
from blueprints.models.steps import Step
from config import Config

blueprint = Blueprint("step", __name__)


def serialize_step(step):
    return {
        "step_id": step.id,
        "step_name": step.name,
        "step_text": step.text,
        "start_date": step.start_date,
        "end_date": step.end_date,
        "image_path": step.image_path,
    }


@blueprint.get("/step/<int:step_id>")
@login_required
def return_specific_step(step_id):
    # show the post with the given id if it's the right user
    step = Step.query.filter_by(user_id=current_user.id, id=step_id)
    if step is not None:
        return serialize_step(step)
    else:
        abort(404)


@blueprint.get("/post/<int:post_id>/step")
@login_required
def return_steps_from_post(post_id):
    # Test if user can access step
    post = Post.query.filter_by(user_id=current_user.id, id=post_id).first()
    if post is None:
        abort(400)

    steps = Step.query.filter_by(post_id=post_id).all()
    if len(steps) > 0:
        return {
            "post": deserialize_post(post),
            "steps": [serialize_step(step) for step in steps],
        }
    else:
        abort(404)


@blueprint.get("/post/<int:post_id>/step/<int:step_id>")
@login_required
def return_step(post_id, step_id):
    # Test if user can access step
    if Post.query.filter_by(user_id=current_user.id, id=post_id).first() is None:
        abort(400)

    steps = Step.query.filter_by(post_id=post_id, id=step_id).all()
    if len(steps) > 0:
        return [serialize_step(step) for step in steps]
    else:
        abort(404)


@blueprint.post("/post/<int:post_id>/step")
@login_required
def create_step(post_id):
    # Test if post is own by the user
    if len(Post.query.filter_by(user_id=current_user.id, id=post_id).all()) == 0:
        abort(400)

    step = Step(
        post_id=post_id,
        name=request.form["name"],
        start_date=datetime.datetime.fromisoformat(request.form["start_date"]),
        end_date=(
            datetime.datetime.fromisoformat(request.form["end_date"])
            if "end_date" in request.form
            else None
        ),
        text=request.form["text"],
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

            step_image = ImageFile(
                name=filename_uploaded,
                image_path=resized_image_path,
                user_id=current_user.id,
            )
            db.session.add(step_image)
            db.session.commit()
            step.image_path = url_for("images.return_image", image_id=step_image.id)

            # Remove tmp files
            os.remove(tmp_path)
        except Exception as e:
            # Delete tmp images if something is wrong
            logging.error(e)
            logging.info(filename_uploaded, step.post_id)
            os.remove(tmp_path)
            os.remove(resized_image_path)

    db.session.add(step)
    db.session.commit()

    return serialize_step(step)
