from flask import Blueprint, jsonify, request
from app.usecases.tasks_usecase import TasksUseCase
from app.auth.auth_service import authorize

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/api/tasks")

tasks_usecase = TasksUseCase()

@tasks_bp.route("/", methods=["GET"])
@authorize()
def get_tasks():
    userid = request.args.get("userid")
    # userid проверяется в декораторе authorize

    tasks = tasks_usecase.get_tasks_data()
    return jsonify(tasks)
