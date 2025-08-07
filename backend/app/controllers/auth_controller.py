from flask import Blueprint, request, jsonify
from app.auth.auth_service import register_user, login_user, authorize

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')
    
    user, error = register_user(username, password, role)
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"message": "User registered"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    token, error = login_user(username, password)
    if error:
        return jsonify({"error": error}), 401
    return jsonify({"token": token})