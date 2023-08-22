from blueprints.models import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(254), nullable=False)
    email = db.Column(db.String(254), nullable=False)
