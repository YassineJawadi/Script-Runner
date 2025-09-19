import os
from dotenv import load_dotenv

# Load environment variables from .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-jwt-key")


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://myuser:2ErdHmed@user-db:3306/user_db"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "2ErdHmed")  # override for dev


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://myuser:2ErdHmed@user-db:3306/user_db"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "2ErdHmed")  # override for prod
