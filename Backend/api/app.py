"""
backend/api/app.py
───────────────────
Flask application factory.

    from api.app import create_app
    app = create_app()
"""

from flask import Flask
from flask_cors import CORS

from termcolor import colored

from config.settings import SECRET_KEY, FLASK_DEBUG, CORS_ORIGINS, APP_VERSION
from core.logger import get_logger

log = get_logger(__name__)


def create_app() -> Flask:
    """Create, configure and return the Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config["SECRET_KEY"]     = SECRET_KEY
    app.config["DEBUG"]          = FLASK_DEBUG
    app.config["JSON_SORT_KEYS"] = False
    
    print(colored(app.url_map, 'green'))

    # CORS — configurable per environment
    CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS}})

    # ── Blueprints ────────────────────────────────────────────────────────────
    from api.blueprints.dataset import dataset_bp
    from api.blueprints.clean   import clean_bp
    from api.blueprints.profile import profile_bp
    from api.blueprints.report  import report_bp
    from api.blueprints.health  import health_bp

    app.register_blueprint(health_bp,  url_prefix="/api/health")
    app.register_blueprint(dataset_bp, url_prefix="/api/dataset")
    app.register_blueprint(clean_bp,   url_prefix="/api/clean")
    app.register_blueprint(profile_bp, url_prefix="/api/profile")
    app.register_blueprint(report_bp,  url_prefix="/api/report")

    log.info("Flask app v%s — 5 blueprints registered", APP_VERSION)
    return app