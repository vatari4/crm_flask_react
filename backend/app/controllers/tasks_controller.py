# app/api/tasks.py
from flask import Blueprint, jsonify, request
from app.usecases.tasks_usecase import TasksUseCase
from app.auth.auth_service import authorize

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/api/tasks")
tasks_usecase = TasksUseCase()

@tasks_bp.route("", methods=["OPTIONS"])
def tasks_options():
    return '', 200

@tasks_bp.route("", methods=["GET"])
@authorize()
def get_user_tasks(current_user):
    if current_user.role == "Администратор":  # допустим роль "Администратор"
        tasks = tasks_usecase.get_all_tasks()
    else:
        tasks = tasks_usecase.get_tasks_data_for_user(current_user.id)
    return jsonify(tasks)

@tasks_bp.route("/optimize", methods=["GET"])
@authorize(required_role="Администратор")
def optimize_tasks(current_user):
    distribution = tasks_usecase.optimize_distribution()
    return jsonify(distribution)

@tasks_bp.route("/update_status", methods=["POST"])
@authorize()
def update_status(current_user):
    data = request.json
    task_id = data.get("task_id")
    new_status = data.get("completion_status")

    if not task_id or not new_status:
        return jsonify({"error": "task_id и completion_status обязательны"}), 400

    task, error = tasks_usecase.update_task_completion_status(task_id, new_status)
    if error:
        return jsonify({"error": error}), 404

    return jsonify({
        "message": "Статус задачи обновлен",
        "task_id": task.id,
        "completion_status": task.completion_status
    })
