from flask import Blueprint, request, jsonify
from app.usecases.contract_usecases import ContractUseCase
from app.repositories.contract_repository import ContractRepository
from app.auth.auth_service import authorize

contract_bp = Blueprint("contract", __name__, url_prefix="/api/contracts")

usecase = ContractUseCase(ContractRepository())

# Получить список контрактов (админ — все, остальные — свои)
@contract_bp.route("/", methods=["GET"])
@authorize()
def get_all_contracts(current_user):
    contracts = usecase.list_contracts(current_user)
    return jsonify([
        {
            "id": c.id,
            "contract_number": c.contract_number,
            "title": c.title,
            "status": c.status,
            "user_id": c.user_id,
            "manager_id": c.manager_id,
            "amount": str(c.amount) if c.amount else None,
            "start_date": c.start_date.isoformat() if c.start_date else None,
            "end_date": c.end_date.isoformat() if c.end_date else None,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "updated_at": c.updated_at.isoformat() if c.updated_at else None,
        }
        for c in contracts
    ])


# Получить один контракт по ID
@contract_bp.route("/<int:contract_id>", methods=["GET"])
@authorize()
def get_contract(current_user, contract_id):
    contract = usecase.get_contract(contract_id)
    if not contract:
        return jsonify({"error": "Контракт не найден"}), 404

    # Проверка доступа
    if current_user.role != "Администратор" and contract.user_id != current_user.id:
        return jsonify({"error": "Доступ запрещен"}), 403

    return jsonify({
        "id": contract.id,
        "contract_number": contract.contract_number,
        "title": contract.title,
        "status": contract.status,
        "user_id": contract.user_id,
        "manager_id": contract.manager_id,
        "amount": str(contract.amount) if contract.amount else None,
        "start_date": contract.start_date.isoformat() if contract.start_date else None,
        "end_date": contract.end_date.isoformat() if contract.end_date else None,
        "created_at": contract.created_at.isoformat() if contract.created_at else None,
        "updated_at": contract.updated_at.isoformat() if contract.updated_at else None,
        "comments": contract.comments,
        "documents_url": contract.documents_url
    })


# Создать новый контракт
@contract_bp.route("/", methods=["POST"])
@authorize()
def create_contract(current_user):
    data = request.get_json()
    data['user_id'] = current_user.id  # Назначаем текущего пользователя владельцем
    contract = usecase.create_contract(data)
    return jsonify({"message": "Контракт создан", "contract_id": contract.id}), 201


# Обновить контракт
@contract_bp.route("/<int:contract_id>", methods=["PUT"])
@authorize()
def update_contract(current_user, contract_id):
    contract = usecase.get_contract(contract_id)
    if not contract:
        return jsonify({"error": "Контракт не найден"}), 404

    if current_user.role != "Администратор" and contract.user_id != current_user.id:
        return jsonify({"error": "Доступ запрещен"}), 403

    data = request.get_json()
    updated = usecase.update_contract(contract_id, data)
    return jsonify({"message": "Контракт обновлён"})


# Удалить контракт
@contract_bp.route("/<int:contract_id>", methods=["DELETE"])
@authorize(required_role="Администратор")
def delete_contract(current_user, contract_id):
    success = usecase.delete_contract(contract_id)
    if not success:
        return jsonify({"error": "Контракт не найден"}), 404
    return jsonify({"message": "Контракт удалён"})


# Изменить статус контракта
@contract_bp.route("/<int:contract_id>/status", methods=["POST"])
@authorize()
def change_status(current_user, contract_id):
    data = request.get_json()
    new_status = data.get("new_status")
    comment = data.get("comment", "")

    contract = usecase.change_status(
        contract_id,
        new_status=new_status,
        user_id=current_user.id,
        comment=comment
    )

    if not contract:
        return jsonify({"error": "Контракт не найден"}), 404

    return jsonify({"message": "Статус обновлён", "new_status": new_status})
