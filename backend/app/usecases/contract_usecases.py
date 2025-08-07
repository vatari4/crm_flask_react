from app.repositories.contract_repository import ContractRepository

class ContractUseCase:
    def __init__(self, repository: ContractRepository):
        self.repo = repository

    def list_contracts(self, user):
        if user.role == 'Администратор':
            return self.repo.get_all()
        else:
            return self.repo.get_by_user(user.id)

    def get_contract(self, contract_id):
        return self.repo.get_by_id(contract_id)

    def create_contract(self, data):
        return self.repo.create(data)

    def update_contract(self, contract_id, data):
        contract = self.repo.get_by_id(contract_id)
        if not contract:
            return None
        return self.repo.update(contract, data)

    def delete_contract(self, contract_id):
        contract = self.repo.get_by_id(contract_id)
        if not contract:
            return False
        self.repo.delete(contract)
        return True

    def change_status(self, contract_id, new_status, user_id, comment=None):
        contract = self.repo.get_by_id(contract_id)
        if not contract:
            return None
        old_status = contract.status
        contract.status = new_status
        self.repo.update(contract, {'status': new_status})
        history = {
            "contract_id": contract_id,
            "old_status": old_status,
            "new_status": new_status,
            "changed_by_id": user_id,
            "comment": comment
        }
        self.repo.add_status_history(history)
        return contract
