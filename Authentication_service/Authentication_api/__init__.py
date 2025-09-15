from flask import Flask
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
login_manager = LoginManager()


def create_app(config_object=None):
    app = Flask(__name__)


    if config_object:
        app.config.from_object(config_object)
    else:
        env_config = os.environ.get("CONFIGURATION_SETUP", "Authentication_service.config")
        app.config.from_object(env_config)


    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "user_blueprint.login"


    from .user_api import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/api")

    return app
