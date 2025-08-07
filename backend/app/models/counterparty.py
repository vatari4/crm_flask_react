from datetime import datetime
from app.db.database import db

class Counterparty(db.Model):
    __tablename__ = "counterparties"

    id = db.Column(db.Integer, primary_key=True)
    legal_form = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(500), nullable=False)
    company_group = db.Column(db.String(200), nullable=True)
    inn = db.Column(db.String(12), nullable=False, unique=True)
    kpp = db.Column(db.String(9), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Counterparty {self.short_name} ({self.legal_form})>"