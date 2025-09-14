# config.py
import os
from dotenv import load_dotenv

# Load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    """Base config shared across environments"""
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecret")


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    # Use the DB URI from .env, fallback to local docker MySQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "mysql+pymysql://root:2ErdHmed%40glsi@localhost:3306/db"
    )
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
    # In production you’d likely connect by container name, not localhost
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "mysql+pymysql://root:2ErdHmed%40glsi@mysql:3306/db"
    )
    SQLALCHEMY_ECHO = False
