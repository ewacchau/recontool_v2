from flask import Flask
from .config import Config
from .extensions import db, migrate, csrf_protect, limiter, celery_init_app

def create_app(config_class: type[Config] = Config):
    app = Flask(__name__)
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
