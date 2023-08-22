import datetime
from blueprints.models import db

class PostImageFile(db.Model):
    __tablename__ = "postimagefile"
    id = db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False) #Actual data, needed for Download
    rendered_data = db.Column(db.Text, nullable=False)#Data to render the pic in browser
    pic_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
