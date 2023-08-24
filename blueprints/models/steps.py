from blueprints.models import db


class Step(db.Model):
    __tablename__ = "step"
    id = db.Column(db.Integer, primary_key=True)
    post_id: db.Mapped[int] = db.mapped_column(
        db.ForeignKey("post.id", ondelete="CASCADE")
    )
    name = db.Column(db.String(254), nullable=False)
    text = db.Column(db.Text(), nullable=True)
    start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(timezone=True), nullable=True)
    image_path = db.Column(db.String(254), nullable=True)
