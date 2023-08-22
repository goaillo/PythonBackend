import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # TODO Change to env var for prod
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
    #     or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = "mysql://root:gaelkevin0109@127.0.0.1:3306/PostsDB"