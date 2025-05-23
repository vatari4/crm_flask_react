from app.db.database import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.LargeBinary(128), nullable=False)  # Храним как байты bcrypt
    role = db.Column(db.String(20), nullable=False)
