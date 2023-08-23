import datetime

from blueprints.models import db


class PostImageFile(db.Model):
    __tablename__ = "postimagefile"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(254), nullable=False)
    image_path = db.Column(
        db.String(254), nullable=False
    )  # Actual data, needed for Download
    pic_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now(datetime.timezone.utc),
    )
