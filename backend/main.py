from flask import Flask
from flask_cors import CORS
from app.db.database import db
from app.config import Config

# Импорт blueprint'ов
from app.controllers.data_controller import data_bp
from app.controllers.tasks_controller import tasks_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)

    app.register_blueprint(data_bp)
    app.register_blueprint(tasks_bp)

    return app

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run(port=5000, debug=True)
