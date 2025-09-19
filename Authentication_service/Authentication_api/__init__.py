# Authentication_api/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os
import importlib

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_object=None):
    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)
    else:
        config_path = os.environ.get("CONFIGURATION_SETUP", "config.DevelopmentConfig")
        module_name, class_name = config_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        config_class = getattr(module, class_name)
        app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    from .user_api import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/user_api")

    return app
