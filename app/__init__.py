from flask import Flask, render_template
from app.routes import bp as routes_bp
from app.models import db
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    app.register_blueprint(routes_bp)

    db.init_app(app)  # <-- initialize database

    with app.app_context():
        db.create_all()  # <-- create tables if they don't exist

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
