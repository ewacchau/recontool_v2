import os


class Config:
    # Core secrets and DB
    SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///recon.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # Celery / Redis
    # Default to Docker Compose service names; override in .env for local venv
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", CELERY_BROKER_URL)

    # Rate limiting
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "redis://redis:6379/1")

    # Third-party APIs
    SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")

    # Cookie / security (overridden in ProductionConfig)
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
    REMEMBER_COOKIE_SECURE = os.getenv("REMEMBER_COOKIE_SECURE", "false").lower() == "true"
    PREFERRED_URL_SCHEME = os.getenv("PREFERRED_URL_SCHEME", "http")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # Fail fast if SECRET_KEY is not set explicitly in prod
    SECRET_KEY = os.getenv("SECRET_KEY")
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = "https"
