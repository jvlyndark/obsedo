import time

from flask import Flask, render_template, request, Response
from flask_migrate import Migrate
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from app.routes import bp as routes_bp
from app.models import db
from app.config import Config
from dotenv import load_dotenv

# Load .env first, then .env.local (which overrides .env)
load_dotenv()
load_dotenv(".env.local", override=True)

# Module-level metrics — defined once to avoid duplicate registration
_REQUEST_COUNT = Counter(
    "flask_http_request_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)
_REQUEST_LATENCY = Histogram(
    "flask_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)
_REQUEST_IN_PROGRESS = Gauge(
    "flask_http_request_in_progress",
    "HTTP requests currently in progress",
    ["method", "path"],
)


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(Config)

    app.register_blueprint(routes_bp)

    db.init_app(app)
    Migrate(app, db)  # Initialize Flask-Migrate

    # Only create tables if not using migrations in production
    if app.config.get("TESTING"):
        with app.app_context():
            db.create_all()

    @app.before_request
    def _before():
        request._prom_start = time.time()
        _REQUEST_IN_PROGRESS.labels(method=request.method, path=request.path).inc()

    @app.after_request
    def _after(response):
        _REQUEST_LATENCY.labels(method=request.method, path=request.path).observe(
            time.time() - request._prom_start
        )
        _REQUEST_COUNT.labels(
            method=request.method, path=request.path, status=response.status_code
        ).inc()
        _REQUEST_IN_PROGRESS.labels(method=request.method, path=request.path).dec()
        return response

    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
