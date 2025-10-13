from flask import Flask

def create_app():
    app = Flask(__name__)
    # load config from app.config (hardcoded values there)
    app.config.from_object("app.config.Config")
    # register blueprints
    from .routes.qa_routes import qa_blueprint
    app.register_blueprint(qa_blueprint, url_prefix="/api/qa")
    return app
