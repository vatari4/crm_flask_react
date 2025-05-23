from app.db.database import db

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    assignee = db.Column(db.String(100))
    due_date = db.Column(db.String(20))
    status = db.Column(db.String(50))
    priority = db.Column(db.String(50))


class TasksMetadata(db.Model):
    __tablename__ = "tasks_metadata"

    id = db.Column(db.Integer, primary_key=True)
    total_tasks = db.Column(db.Integer)
    tasks_in_progress = db.Column(db.Integer)
    tasks_completed = db.Column(db.Integer)
    generated_at = db.Column(db.String(50))
