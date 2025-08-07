from collections import defaultdict
import random
import statistics
from app.models.task import Task
from app.models.tasks_metadata import TasksMetadata
from app.models.user import User

class TasksRepository:
    @staticmethod
    def get_tasks_for_user(user_id):
        tasks = Task.query.filter_by(user_id=user_id).all()
        metadata = TasksMetadata.query.filter_by(user_id=user_id).first()

        return {
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "due_date": task.due_date,
                    "status": task.status,
                    "priority": task.priority,
                    "completion_status": task.completion_status
                }
                for task in tasks
            ],
            "metadata": {
                "total_tasks": metadata.total_tasks if metadata else 0,
                "tasks_in_progress": metadata.tasks_in_progress if metadata else 0,
                "tasks_completed": metadata.tasks_completed if metadata else 0,
                "generated_at": metadata.generated_at if metadata else None,
            }
        }

    @staticmethod
    def get_all_tasks():
        tasks = Task.query.all()

        return {
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "due_date": task.due_date,
                    "status": task.status,
                    "priority": task.priority,
                    "user_id": task.user_id,
                    "completion_status": task.completion_status
                }
                for task in tasks
            ]
        }

    @staticmethod
    def optimize_task_distribution(tasks, available_users):
        """
        Распределяет задачи между пользователями, минимизируя дисперсию загрузки.
        Учитываются только задачи без статуса выполнения (т.е. задачи в работе).
        """
        # Фильтруем задачи, которые еще не имеют completion_status
        pending_tasks = [task for task in tasks if not task.completion_status]

        prioritized_tasks = sorted(
            pending_tasks,
            key=lambda x: (x.priority == 'high', x.due_date),
            reverse=True
        )

        simulation_results = []

        for _ in range(100):
            random.shuffle(prioritized_tasks)
            workload_map = defaultdict(list)

            # Простая round-robin модель распределения
            for i, task in enumerate(prioritized_tasks):
                user = available_users[i % len(available_users)]
                workload_map[user.id].append(task)

            simulation_results.append(
                TasksRepository._calculate_workload(workload_map)
            )

        optimal_distribution = min(simulation_results, key=lambda x: x['variance'])

        # Возвращаем dict: user_id -> list of task ids
        return optimal_distribution['tasks_by_user']

    @staticmethod
    def _calculate_workload(workload_map):
        task_counts = [len(tasks) for tasks in workload_map.values()]
        variance = statistics.variance(task_counts) if len(task_counts) > 1 else 0

        return {
            "variance": variance,
            "tasks_by_user": {
                user_id: [task.id for task in tasks]
                for user_id, tasks in workload_map.items()
            }
        }