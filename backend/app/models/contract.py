from datetime import datetime
from app.db.database import db

class Contract(db.Model):
    __tablename__ = "contracts"

    id = db.Column(db.Integer, primary_key=True)

    # Основная информация
    contract_number = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)

    # Статус контракта
    status = db.Column(
        db.String(50),
        nullable=False,
        default='в стадии сделки',
        info={
            'choices': [
                'подписан',
                'готов к подписанию',
                'сбор данных',
                'в стадии сделки',
                'отказ'
            ]
        }
    )

    # Предприятие
    legal_entity_name = db.Column(db.String(200), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)

    # Даты
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    counterparty_id = db.Column(db.Integer, db.ForeignKey('counterparties.id'), nullable=True)

    # Дополнительная информация
    comments = db.Column(db.Text, nullable=True)
    documents_url = db.Column(db.String(255), nullable=True)

    # Сумма контракта
    amount = db.Column(db.Numeric(12, 2), nullable=True)

    # Отношения
    user = db.relationship('User', foreign_keys=[user_id], backref='contracts')
    manager = db.relationship('User', foreign_keys=[manager_id])
    counterparty = db.relationship('Counterparty', backref='contracts')

    def __repr__(self):
        return f"<Contract {self.contract_number} ({self.status})>"


class ContractStatusHistory(db.Model):
    __tablename__ = "contract_status_history"

    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=False)
    old_status = db.Column(db.String(50))
    new_status = db.Column(db.String(50))
    changed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    change_date = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.Text)

    contract = db.relationship('Contract', backref='status_history')
    changed_by = db.relationship('User')

    def __repr__(self):
        return f"<StatusChange {self.old_status}->{self.new_status} for Contract {self.contract_id}>"