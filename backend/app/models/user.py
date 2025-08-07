from app.db.database import db
from datetime import datetime, date
from app.models.role import Role  
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)

    employment_start_date = db.Column(db.Date, nullable=True)
    employment_end_date = db.Column(db.Date, nullable=True)

    service_duration_days = db.Column(db.Integer, default=0)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', back_populates='users')

    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    subordinates = db.relationship(
        'User',
        backref=db.backref('manager', remote_side=[id]),
        lazy='dynamic'
    )

    # Предположительно:
    tasks = db.relationship('Task', back_populates='user', lazy='dynamic')
    tasks_metadata = db.relationship('TasksMetadata', back_populates='user', uselist=False)

    def full_name(self):
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return " ".join(parts)

    def __repr__(self):
        return f"<User {self.username} ({self.full_name()}) Role: {self.role.name}>"
