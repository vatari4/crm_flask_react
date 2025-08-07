from flask import Blueprint, request, jsonify
from app.auth.auth_service import authorize
from app.repositories.user_repository import UserRepository
from app.usecases.user_usecase import UserUseCase

user_bp = Blueprint("user", __name__, url_prefix="/api/auth/admin")

user_repo = UserRepository()
user_usecase = UserUseCase(user_repo)


@user_bp.route('/users', methods=['GET'])
@authorize(required_role="Администратор")
def get_all_users(current_user):
    result = user_usecase.list_users()
    return jsonify(result)


@user_bp.route('/users/<int:user_id>', methods=['GET'])
@authorize(required_role="Администратор")
def get_user(current_user, user_id):
    user_data = user_usecase.get_user(user_id)
    if not user_data:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user_data)


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@authorize(required_role="Администратор")
def update_user(current_user, user_id):
    data = request.json
    try:
        user_usecase.update_user(user_id, data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"message": "User updated successfully"})


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@authorize(required_role="Администратор")
def delete_user(current_user, user_id):
    try:
        user_usecase.delete_user(user_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    return jsonify({"message": "User deleted successfully"})
