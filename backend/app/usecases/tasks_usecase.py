from app.repositories.tasks_repository import TasksRepository
from app.models.task import Task
from app.models.user import User

class TasksUseCase:
    def __init__(self):
        self.repo = TasksRepository()

    def get_tasks_data_for_user(self, user_id):
        return self.repo.get_tasks_for_user(user_id)

    def get_all_tasks(self):
        return self.repo.get_all_tasks()

    def optimize_distribution(self):
        tasks = Task.query.all()
        users = User.query.all()
        return self.repo.optimize_task_distribution(tasks, users)

    def update_task_completion_status(self, task_id, new_status):
        task = Task.query.get(task_id)
        if not task:
            return None, "Task not found"
        task.completion_status = new_status
        from app.db.database import db
        db.session.commit()
        return task, None