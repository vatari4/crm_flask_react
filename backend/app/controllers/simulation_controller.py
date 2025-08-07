from flask import Blueprint, jsonify, request
from app.simulation.simulation_service import SimulationService
from app.auth.auth_service import authorize

simulation_bp = Blueprint('simulation_bp', __name__, url_prefix='/api/simulation')

@simulation_bp.route('/client-requests', methods=['POST'])
@authorize(roles=['admin', 'manager'])
def simulate_client_requests(current_user):
    """
    Эндпоинт для имитации клиентских запросов
    """
    params = request.get_json()
    tasks = SimulationService.simulate_client_requests(
        current_user.id,
        params
    )
    return jsonify({
        "status": "success",
        "tasks_generated": len(tasks),
        "reference": "Имитационное моделирование, 2024"
    })