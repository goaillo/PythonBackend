from blueprints.models import db

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    user_id: db.Mapped[int] = db.mapped_column(db.ForeignKey("user.id"))
    name = db.Column(db.String(254), nullable=False)
    start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(timezone=True), nullable=True)
    image_id = db.Column(db.Integer, db.ForeignKey('postimagefile.id'))
    image = db.relationship("PostImageFile", backref=db.backref("post", uselist=False))