from db import db


class TaskModel(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(80), unique=False, nullable=False)
    report_name = db.Column(db.String(100), unique=False, nullable=True)
    author = db.Column(db.String(80), unique=False, nullable=False)
    schedule_type = db.Column(db.String(80), unique=False, nullable=False)
    time_trigger_interval = db.Column(db.String(80), unique=False, nullable=True)
    calendar_trigger_days = db.Column(db.String(80), unique=False, nullable=True)
    calendar_trigger_weeks_interval = db.Column(db.Integer)
    execution_time = db.Column(db.DateTime, unique=False, nullable=True)