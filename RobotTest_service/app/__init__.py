import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")
    if env == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import routes and register blueprints
    from .routes import robot_bp
    app.register_blueprint(robot_bp, url_prefix="/robotTest")

    return app
