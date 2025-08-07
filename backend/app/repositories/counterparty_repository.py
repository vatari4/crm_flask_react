from app.models.counterparty import Counterparty
from app.db.database import db

class CounterpartyRepository:
    def get_all(self):
        return Counterparty.query.all()

    def get_by_id(self, counterparty_id):
        return Counterparty.query.get(counterparty_id)

    def get_by_inn(self, inn):
        return Counterparty.query.filter_by(inn=inn).first()

    def create(self, data):
        counterparty = Counterparty(**data)
        db.session.add(counterparty)
        db.session.commit()
        return counterparty

    def update(self, counterparty, updates):
        for key, value in updates.items():
            setattr(counterparty, key, value)
        db.session.commit()
        return counterparty

    def delete(self, counterparty):
        db.session.delete(counterparty)
        db.session.commit()