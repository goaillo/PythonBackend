import datetime

from blueprints.models import db


class ImageFile(db.Model):
    __tablename__ = "ImageFile"
    id = db.Column(db.Integer, primary_key=True)
    user_id: db.Mapped[int] = db.mapped_column(
        db.ForeignKey("user.id", ondelete="CASCADE")
    )
    name = db.Column(db.String(254), nullable=False)
    image_path = db.Column(
        db.String(254), nullable=False
    )  # Actual data, needed for Download
    pic_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now(datetime.timezone.utc),
    )
