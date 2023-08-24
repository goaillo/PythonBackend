import os
from io import BytesIO

from flask import Flask, send_file
from flask_login import LoginManager
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.security import generate_password_hash

from blueprints.documented_endpoints.auth import auth as auth_endpoints
from blueprints.documented_endpoints.images import blueprint as images_endpoints
from blueprints.documented_endpoints.posts import blueprint as posts_endpoints
from blueprints.documented_endpoints.steps import blueprint as steps_endpoints
from blueprints.documented_endpoints.users import blueprint as users_endpoints
from blueprints.models import db
from blueprints.models.user import User
from config import Config

# create the Flask app
app = Flask(__name__)

# configure the Flask app
app.config["SQLALCHEMY_DATABASE_URI"] = Config.SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"] = Config.SECRET_KEY

# create dir for work

if not os.path.exists(Config.TMP_FOLDER):
    os.makedirs(Config.TMP_FOLDER)
if not os.path.exists(Config.FILES_FOLDER):
    os.makedirs(Config.FILES_FOLDER)

db.init_app(app)

# Create database and tables with the models in models/
with app.app_context():
    db.drop_all()
    db.create_all()

    # Create Root User (if not exists)
    if len(User.query.filter_by(email=Config.ADMIN_EMAIL).all()) == 0:
        db.session.add(
            User(
                email=Config.ADMIN_EMAIL,
                username="admin",
                password=generate_password_hash(Config.ADMIN_PASSWORD, method="scrypt"),
                is_admin=True,
            )
        )
        db.session.commit()

# Create Swagger
SWAGGER_URL = "/docs"  # URL for exposing Swagger UI (without trailing '/')
# TODO Modify for production
API_URL = "http://127.0.0.1:5000/swagger.yml"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={"app_name": "Posts application"},  # Swagger UI config overrides
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)


# blueprint for auth routes in our app
# from .auth import auth as auth_blueprint
# app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
# from .main import main as main_blueprint
# app.register_blueprint(main_blueprint)

app.register_blueprint(swaggerui_blueprint)
app.register_blueprint(posts_endpoints)
app.register_blueprint(steps_endpoints)
app.register_blueprint(users_endpoints)
app.register_blueprint(images_endpoints)
app.register_blueprint(auth_endpoints)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


# Serve Swagger file
@app.route("/swagger.yml")
def swagger():
    with open(os.path.join(os.path.dirname(__file__), "swagger.yml"), "rb") as f:
        return send_file(BytesIO(f.read()), mimetype="text/yaml")


if __name__ == "__main__":
    app.run()
