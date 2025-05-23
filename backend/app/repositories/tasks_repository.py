from app.models.task import Task, TasksMetadata

class TasksRepository:
    @staticmethod
    def get_tasks():
        tasks = Task.query.all()
        metadata = TasksMetadata.query.first()

        return {
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "assignee": task.assignee,
                    "due_date": task.due_date,
                    "status": task.status,
                    "priority": task.priority,
                } for task in tasks
            ],
            "metadata": {
                "total_tasks": metadata.total_tasks,
                "tasks_in_progress": metadata.tasks_in_progress,
                "tasks_completed": metadata.tasks_completed,
                "generated_at": metadata.generated_at,
            }
        }
