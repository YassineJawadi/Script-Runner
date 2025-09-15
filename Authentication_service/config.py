import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
class config:
    SECRET_KEY = "your secret key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("mysql+pymysql://root:secret%40glsi@localhost:3306/db")
    SQLALCHEMY_ECHO = True

class ProductionConfig(config):
    DEBUG =False
    SQLALCHEMY_DATABASE_URI = os.environ.get("mysql+pymysql://root:secret%40glsi@localhost:3306/db")
    SQLALCHEMY_ECHO = False
