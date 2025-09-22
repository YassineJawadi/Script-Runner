import os

class Config:
    """Base configuration (shared across environments)."""
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-jwt-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development environment config."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment config."""
    DEBUG = False
    TESTING = False
    # Example: enable stricter cookies
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True


# Map environments for factory use
config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig
)
