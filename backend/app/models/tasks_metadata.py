from app.db.database import db
from datetime import datetime

class TasksMetadata(db.Model):
    __tablename__ = "tasks_metadata"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total_tasks = db.Column(db.Integer, default=0)
    tasks_in_progress = db.Column(db.Integer, default=0)
    tasks_completed = db.Column(db.Integer, default=0)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="tasks_metadata")

    def __repr__(self):
        return f"<TasksMetadata User {self.user_id} - Completed: {self.tasks_completed}>"
