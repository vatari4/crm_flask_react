from app.repositories.data_repository import DataRepository
from app.db.database import db
from app.models.user import User

class DataUseCase:
    def __init__(self):
        self.repo = DataRepository()

    def get_analytics_data_for_user(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}

        if user.role == "admin":
            # Получаем всех подчинённых админа
            subordinates = user.subordinates.all()
            data_for_subordinates = []
            for subordinate in subordinates:
                data = self.repo.get_analytics_for_user(subordinate.id)
                data_for_subordinates.append({
                    "user_id": subordinate.id,
                    "username": subordinate.username,
                    "data": data
                })
            return {"subordinates_data": data_for_subordinates}
        else:
            # Обычный пользователь — только свои данные
            return self.repo.get_analytics_for_user(user_id)

    def get_all_analytics_data(self):
        all_users = User.query.all()
        all_data = []
        
        for user in all_users:
            user_data = self.repo.get_analytics_for_user(user.id)
            all_data.append({
                "user_id": user.id,
                "username": user.username,
                "role": user.role,
                "data": user_data
            })
        
        return {"all_users_data": all_data}