from app.models.user import User, Role
from app.db.database import db
from datetime import datetime

class UserRepository:

    def get_all(self):
        return User.query.all()

    def get_by_id(self, user_id: int):
        return User.query.get(user_id)

    def get_role_by_name(self, role_name: str):
        return Role.query.filter_by(name=role_name).first()

    def get_user_tasks_completed_successfully_count(self, user: User):
        return user.tasks.filter_by(completion_status="Выполнил успешно").count()

    def update_user(self, user: User, data: dict):
        if 'username' in data:
            user.username = data['username']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'middle_name' in data:
            user.middle_name = data['middle_name']

        if 'employment_start_date' in data:
            try:
                user.employment_start_date = datetime.strptime(data['employment_start_date'], "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid employment_start_date format. Expected YYYY-MM-DD")

        if 'employment_end_date' in data:
            try:
                user.employment_end_date = datetime.strptime(data['employment_end_date'], "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid employment_end_date format. Expected YYYY-MM-DD")

        if 'role' in data:
            role = self.get_role_by_name(data['role'])
            if not role:
                raise ValueError("Role not found")
            user.role = role

        if 'manager_id' in data:
            if data['manager_id'] is not None:
                manager = self.get_by_id(data['manager_id'])
                if not manager:
                    raise ValueError("Manager user not found")
            user.manager_id = data['manager_id']

        db.session.commit()

    def delete_user(self, user: User):
        db.session.delete(user)
        db.session.commit()
        
    def save(self, user: User):
        db.session.add(user)
        db.session.commit()
