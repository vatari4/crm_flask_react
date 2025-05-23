import os
from datetime import datetime, timedelta
from functools import wraps

import bcrypt
import jwt
from flask import request, jsonify
from app.models.user import User
from app.db.database import db

JWT_SECRET = os.getenv("SECRET_KEY", "supersecretkey")
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 3600  # 1 час

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def generate_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
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
            
            if required_role and user.role != required_role:
                return jsonify({"error": "Forbidden"}), 403
            
            # Добавляем user в kwargs, если нужно
            kwargs['user'] = user
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
    token = generate_token(user.id, user.role)
    return token, None
