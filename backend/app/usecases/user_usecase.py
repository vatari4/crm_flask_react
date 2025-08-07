from datetime import date
from app.repositories.user_repository import UserRepository

class UserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def _update_service_duration(self, user):
        if user.employment_start_date:
            end_date = user.employment_end_date or date.today()
            user.service_duration_days = (end_date - user.employment_start_date).days
            self.user_repo.save(user)  # сохранение изменений в репозитории

    def list_users(self):
        users = self.user_repo.get_all()
        for u in users:
            self._update_service_duration(u)
        return [self._user_to_dict(u) for u in users]

    def get_user(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            return None
        self._update_service_duration(user)
        return self._user_to_dict(user)

    def update_user(self, user_id: int, data: dict):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        self.user_repo.update_user(user, data)
        # Обновим срок службы после обновления данных (т.к. мог измениться start/end date)
        self._update_service_duration(user)

    def delete_user(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        self.user_repo.delete_user(user)

    def _user_to_dict(self, u):
        return {
            "id": u.id,
            "username": u.username,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "middle_name": u.middle_name,
            "employment_start_date": u.employment_start_date.isoformat() if u.employment_start_date else None,
            "employment_end_date": u.employment_end_date.isoformat() if u.employment_end_date else None,
            "service_duration_days": u.service_duration_days,
            "role": u.role.name if u.role else None,
            "manager_id": u.manager_id,
            "manager_username": u.manager.username if u.manager else None,
            "tasks_completed_successfully": self.user_repo.get_user_tasks_completed_successfully_count(u),
        }
