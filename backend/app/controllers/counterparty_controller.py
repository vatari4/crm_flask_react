from flask import Blueprint, request, jsonify
from app.auth.auth_service import authorize
from app.usecases.counterparty_usecases import CounterpartyUseCase
from app.repositories.counterparty_repository import CounterpartyRepository

counterparty_bp = Blueprint("counterparty", __name__, url_prefix="/api/counterparties")

usecase = CounterpartyUseCase(CounterpartyRepository())

@counterparty_bp.route("", methods=["GET"])
@authorize()
def get_all_counterparties(current_user):
    counterparties = usecase.list_counterparties()
    return jsonify([
        {
            "id": c.id,
            "legal_form": c.legal_form,
            "short_name": c.short_name,
            "full_name": c.full_name,
            "company_group": c.company_group,
            "inn": c.inn,
            "kpp": c.kpp,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "updated_at": c.updated_at.isoformat() if c.updated_at else None,
        }
        for c in counterparties
    ])

@counterparty_bp.route("/<int:counterparty_id>", methods=["GET"])
@authorize()
def get_counterparty(current_user, counterparty_id):
    counterparty = usecase.get_counterparty(counterparty_id)
    if not counterparty:
        return jsonify({"error": "Контрагент не найден"}), 404
    
    return jsonify({
        "id": counterparty.id,
        "legal_form": counterparty.legal_form,
        "short_name": counterparty.short_name,
        "full_name": counterparty.full_name,
        "company_group": counterparty.company_group,
        "inn": counterparty.inn,
        "kpp": counterparty.kpp,
        "created_at": counterparty.created_at.isoformat() if counterparty.created_at else None,
        "updated_at": counterparty.updated_at.isoformat() if counterparty.updated_at else None,
    })

@counterparty_bp.route("", methods=["POST"])
@authorize(required_role="Администратор")
def create_counterparty(current_user):
    data = request.get_json()
    counterparty, error = usecase.create_counterparty(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Контрагент создан", "counterparty_id": counterparty.id}), 201

@counterparty_bp.route("/<int:counterparty_id>", methods=["PUT"])
@authorize(required_role="Администратор")
def update_counterparty(current_user, counterparty_id):
    data = request.get_json()
    counterparty, error = usecase.update_counterparty(counterparty_id, data)
    if error:
        return jsonify({"error": error}), 404
    return jsonify({"message": "Контрагент обновлён"})

@counterparty_bp.route("/<int:counterparty_id>", methods=["DELETE"])
@authorize(required_role="Администратор")
def delete_counterparty(current_user, counterparty_id):
    success = usecase.delete_counterparty(counterparty_id)
    if not success:
        return jsonify({"error": "Контрагент не найден"}), 404
    return jsonify({"message": "Контрагент удалён"})