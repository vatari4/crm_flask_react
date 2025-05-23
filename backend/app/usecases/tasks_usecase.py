from app.repositories.tasks_repository import TasksRepository

class TasksUseCase:
    def __init__(self):
        self.repo = TasksRepository()

    def get_tasks_data(self):
        return self.repo.get_tasks()
