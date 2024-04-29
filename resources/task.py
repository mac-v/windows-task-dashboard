from flask_smorest import Blueprint, abort
from flask.views import MethodView
#from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import TaskModel
from schemas import TaskSchema
blp = Blueprint("Tasks", "task", description="Task management functions")

@blp.route("/task")
class TasksList(MethodView):

    @blp.response(200, TaskSchema(many=True))
    def get(self):
        return TaskModel.query.all()
