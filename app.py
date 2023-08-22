from io import BytesIO
import os

from flask import Flask, send_file
from flask_swagger_ui import get_swaggerui_blueprint

from blueprints.documented_endpoints.posts import blueprint as posts_endpoints
from blueprints.documented_endpoints.steps import blueprint as steps_endpoints
from blueprints.models import db

# create the Flask app
app = Flask(__name__)

# configure the F
# TODO Modify for production
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:gaelkevin0109@127.0.0.1:3306/PostsDB"
db.init_app(app)

# Create database and tables with the models in models/
with app.app_context():
    print("CREATE DATABASE !!!!!!!")
    db.create_all()

# Create Swagger
SWAGGER_URL = '/docs'  # URL for exposing Swagger UI (without trailing '/')
# TODO Modify for production
API_URL = 'http://127.0.0.1:5000/swagger.yml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Posts application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)
app.register_blueprint(posts_endpoints)
app.register_blueprint(steps_endpoints)

# Serve Swagger file
@app.route('/swagger.yml')
def swagger():
    with open(os.path.join(os.path.dirname(__file__), 'swagger.yml'), 'rb') as f:
        return send_file(BytesIO(f.read()), mimetype='text/yaml')

if __name__ == "__main__":
    app.run()
