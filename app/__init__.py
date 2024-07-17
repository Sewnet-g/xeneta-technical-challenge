import json
import logging.config

from flask import Flask

from app import settings


def create_app():
    """
    Application factory for creating Flask apps.
    """
    # Configure logging
    with open(settings.LOGGING_CONFIG, "r") as f:
        logging.config.dictConfig(json.load(f))
    logger = logging.getLogger(__name__)
    logger.debug("Logging configured.")

    # Create Flask app
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config.from_object(settings)
    logger.debug("Configured Flask app.")

    # Initialize database (connection settings)
    from app.database import init_db
    init_db(app)
    logger.debug("Initialized database.")

    # Register blueprints
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    logger.debug("Registered blueprints.")

    return app
