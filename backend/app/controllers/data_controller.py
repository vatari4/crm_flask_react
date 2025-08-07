from flask import Blueprint, jsonify, request
from app.auth.auth_service import authorize
from app.usecases.data_usecase import DataUseCase

data_bp = Blueprint("data_bp", __name__, url_prefix="/api/data")

data_usecase = DataUseCase()

@data_bp.route("", methods=["OPTIONS"])
def data_options():
    return '', 200

@data_bp.route("", methods=["GET"])
@authorize()
def get_user_data(current_user):
    if current_user.role == "admin":
        data = data_usecase.get_all_analytics_data()
    else:
        data = data_usecase.get_analytics_data_for_user(current_user.id)
    return jsonify(data)
