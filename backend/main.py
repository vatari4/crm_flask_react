from flask import Flask
from flask_cors import CORS
from app.db.database import db
from app.config import Config

# Import blueprints
from app.controllers.data_controller import data_bp
from app.controllers.tasks_controller import tasks_bp
from app.controllers.auth_controller import auth_bp
from app.controllers.user_controller import user_bp
from app.controllers.contract_controller import contract_bp
from app.controllers.counterparty_controller import counterparty_bp

# Import admin initialization
from app.db.init_db import create_default_users, create_default_analytics

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    CORS(app, 
         resources={
             r"/api/*": {
                 "origins": "http://localhost:5173",
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
                 "allow_headers": ["Content-Type", "Authorization"],
                 "supports_credentials": True
             }
         })

    app.register_blueprint(data_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(contract_bp)
    app.register_blueprint(counterparty_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()
        create_default_users()
        create_default_analytics()

    app.run(port=5000, debug=True)