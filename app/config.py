import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'defaultsecret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:////app/obsedo.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
