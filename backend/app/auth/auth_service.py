import os
from datetime import datetime, timedelta
from functools import wraps

import bcrypt
import jwt
from flask import request, jsonify
from app.models.user import User
from app.models.role import Role
from app.db.database import db

JWT_SECRET = os.getenv("SECRET_KEY", "supersecretkey")
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 259200

def hash_password(password: str) -> str:
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def generate_token(user_id, role_obj, username, manager_id=None):
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role_obj.name if role_obj else "Пользователь",
        "manager_id": manager_id,
        "exp": datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)



def decode_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def authorize(required_role=None):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization', None)
            if not auth_header:
                return jsonify({"error": "Authorization header missing"}), 401

            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return jsonify({"error": "Invalid authorization header"}), 401

            token = parts[1]
            payload = decode_token(token)
            if not payload:
                return jsonify({"error": "Invalid or expired token"}), 401

            user = db.session.get(User, payload['user_id'])
            if not user:
                return jsonify({"error": "User not found"}), 401

            if required_role and (not user.role or user.role.name != required_role):
                return jsonify({"error": "Forbidden"}), 403

            kwargs['current_user'] = user
            return fn(*args, **kwargs)
        return decorated
    return wrapper


def register_user(username, password, role='user'):
    if db.session.query(User).filter_by(username=username).first():
        return None, "User already exists"
    hashed = hash_password(password)
    new_user = User(username=username, password=hashed, role=role)
    db.session.add(new_user)
    db.session.commit()
    return new_user, None

def login_user(username, password):
    user = db.session.query(User).filter_by(username=username).first()
    if not user or not check_password(password, user.password):
        return None, "Invalid credentials"
    token = generate_token(user.id, user.role, user.username, user.manager_id)
    return token, None


def register_user_by_admin(current_user, username, password, role_name, manager_id=None):
    if current_user.role.name != "Администратор":
        return None, "Недостаточно прав"

    if db.session.query(User).filter_by(username=username).first():
        return None, "Пользователь уже существует"

    role_obj = Role.query.filter_by(name=role_name).first()
    if not role_obj:
        return None, "Роль не найдена"

    hashed = hash_password(password)
    new_user = User(
        username=username,
        password=hashed,
        role=role_obj,
        manager_id=manager_id or current_user.id
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user, None


def update_user_by_admin(current_user, user_id, username=None, role=None, manager_id=None):
    if current_user.role != "Администратор":
        return None, "Недостаточно прав"
    
    user = db.session.get(User, user_id)
    if not user:
        return None, "Пользователь не найден"
    
    if username:
        user.username = username
    if role:
        user.role = role
    if manager_id is not None:  # явная проверка на None, так как manager_id может быть 0
        user.manager_id = manager_id
    
    db.session.commit()
    return user, None

def delete_user_by_admin(current_user, user_id):
    if current_user.role != "Администратор":
        return None, "Недостаточно прав"
    
    user = db.session.get(User, user_id)
    if not user:
        return None, "Пользователь не найден"
    
    db.session.delete(user)
    db.session.commit()
    return True, None