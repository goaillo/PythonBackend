import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # TODO Change to env var for prod
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}:{}/{}".format(
        os.environ.get('DATABASE_USER'),
        os.environ.get('DATABASE_PASSWD'),
        os.environ.get('DATABASE_HOST'),
        os.environ.get('DATABASE_PORT'),
        os.environ.get('DATABASE_NAME'),
    )