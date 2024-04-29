from datetime import datetime

from flask import Flask
from flask_smorest import Api
import os
from db import db
import models.task
from resources.task import blp as TaskBlueprint
from models import TaskModel
from task_manager import retrieve_windows_task

# Factory pattern
def create_app(db_url=None):
    app = Flask(__name__)
    db_file_path = os.path.join(app.instance_path, 'data.db')
    if os.path.exists(db_file_path):
        os.remove(db_file_path)
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
        insert_inititial_data()
        tasks = TaskModel.query.all()

        for task in tasks:
            print(task.task_name, task.report_name, task.author, task.schedule_type, task.time_trigger_interval,
                  task.calendar_trigger_days, task.calendar_trigger_weeks_interval, task.execution_time)

    api.register_blueprint(TaskBlueprint)
    return app

def insert_inititial_data():

    tasks = retrieve_windows_task()
    for task in tasks:
        dict_data = task.to_dict()
        transformed_task = TaskModel(**dict_data)
        db.session.add(transformed_task)
        db.session.commit()
