from app.models.contract import Contract, ContractStatusHistory
from app.db.database import db

class ContractRepository:
    def get_all(self):
        return Contract.query.all()

    def get_by_id(self, contract_id):
        return Contract.query.get(contract_id)

    def create(self, data):
        contract = Contract(**data)
        db.session.add(contract)
        db.session.commit()
        return contract

    def update(self, contract, updates):
        for key, value in updates.items():
            setattr(contract, key, value)
        db.session.commit()
        return contract

    def delete(self, contract):
        db.session.delete(contract)
        db.session.commit()

    def add_status_history(self, history_data):
        history = ContractStatusHistory(**history_data)
        db.session.add(history)
        db.session.commit()
        return history
    
    def get_by_user(self, user_id):
        return Contract.query.filter_by(user_id=user_id).all()
