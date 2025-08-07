from app.db.database import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending')  # pending, in_progress, completed
    priority = db.Column(db.String(20), nullable=False, default='medium')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    completion_status = db.Column(db.String(50), nullable=True, default=None)  # Выполнил успешно, со сложностями, не выполнил и т.д.

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='tasks')

    def __repr__(self):
        return f"<Task {self.title} - User {self.user_id} - Completion: {self.completion_status}>"
