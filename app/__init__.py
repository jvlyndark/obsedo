from flask import Flask, render_template
from app.routes import bp as routes_bp
from app.models import db
from app.config import Config
from dotenv import load_dotenv

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(Config)

    app.register_blueprint(routes_bp)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
