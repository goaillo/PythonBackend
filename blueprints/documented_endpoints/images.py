from io import BytesIO

from flask import Blueprint, abort, send_file
from flask_login import current_user, login_required

from blueprints.models.image_file import ImageFile
from blueprints.models.post import Post

blueprint = Blueprint("images", __name__)


@blueprint.get("/image/<int:image_id>")
@login_required
def return_image(image_id):
    image = ImageFile.query.filter_by(id=image_id, user_id=current_user.id).first()
    if image is None:
        abort(404)

    with open(image.image_path, "rb") as f:
        return send_file(
            BytesIO(f.read()), mimetype="image/jpg", download_name=image.name
        )
