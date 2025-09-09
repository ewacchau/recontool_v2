import os
from flask import Flask
from werkzeug.utils import import_string
from .config import Config
from .extensions import db, migrate, csrf_protect, limiter, celery_init_app

def create_app(config_class: type[Config] | None = None):
    app = Flask(__name__)
    # Allow selecting config via env var APP_CONFIG (e.g., "app.config.ProductionConfig")
    if config_class is None:
        cfg_path = app.config.get("APP_CONFIG") or os.getenv("APP_CONFIG")
        if cfg_path:
            config_class = import_string(cfg_path)
        else:
            config_class = Config
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf_protect.init_app(app)
    limiter.init_app(app)

    # register blueprints
    from .scans import scans_bp
    app.register_blueprint(scans_bp)

    # init celery
    celery_init_app(app)
    return app
