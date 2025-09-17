import os
from flask import Flask
from flask_migrate import Migrate
from .models import db
from .routes import robot_bp       # rename blueprint to robot_bp in routes.py
from config import DevelopmentConfig, ProductionConfig

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(robot_bp, url_prefix="/robotTest")

    return app
