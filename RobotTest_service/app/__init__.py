import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load configuration
    env = os.getenv("FLASK_ENV", "development")
    if env == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import blueprints
    from .routes import robot_bp
    app.register_blueprint(robot_bp, url_prefix="/robotTest")

    return app
