import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "defaultsecret")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    # Use SQLite for local development, PostgreSQL for production
    if os.environ.get("FLASK_ENV") == "production" or os.environ.get("DATABASE_URL"):
        # Production: Use PostgreSQL from environment
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    else:
        # Development: Use SQLite
        SQLALCHEMY_DATABASE_URI = "sqlite:///obsedo.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
