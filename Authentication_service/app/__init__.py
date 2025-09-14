import os
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .models import db
from .Authentication_api.routes import auth_bp

migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")
    if env == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
