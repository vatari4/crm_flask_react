from flask import Blueprint, jsonify, request
from app.usecases.data_usecase import DataUseCase
from app.auth.auth_service import authorize

data_bp = Blueprint("data_bp", __name__, url_prefix="/api/data")

data_usecase = DataUseCase()

@data_bp.route("/", methods=["GET"])
@authorize()
def get_data():
    userid = request.args.get("userid")
    # userid проверяется в декораторе authorize

    data = data_usecase.get_analytics_data()
    return jsonify(data)
