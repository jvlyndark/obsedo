from flask import Flask
from app.routes import bp as routes_bp
from app.models import db  # <-- ADD THIS

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.register_blueprint(routes_bp)

    db.init_app(app)  # <-- ADD THIS

    with app.app_context():
        db.create_all()

    return app
