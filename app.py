from flask import Flask
from flask_smorest import Api
import os
from db import db


# Factory pattern
def create_app(db_url=None):
    app = Flask(__name__)
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = "Reports REST API"
    app.config['API_VERSION'] = "v1"
    app.config['OPENAPI_VERSION'] = "3.0.3"
    app.config['OPENAPI_URL_PREFIX'] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https:/cdn.jsdelivr.net/npm/swagger-ui-dist/"
    ## If env db url does not exists it goes to sql lite
    # Env variable secure our db credentials
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # SQL alchemy creation
    db.init_app(app)

    # Connection flask smorest to flask app
    # Flask smorest
    # 1. Structuring code 2. Adds ons like swagger
    api = Api(app)

    # Creating and building tables defined in models
    with app.app_context():
        db.create_all()

    return app
