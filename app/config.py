import os
class Config:
    SECRET_KEY   = os.getenv("SECRET_KEY", "changeme")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///recon.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
    RATELIMIT_HEADERS_ENABLED = True
