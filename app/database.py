import logging

import psycopg2
from flask import Flask

logger = logging.getLogger(__name__)


def init_db(app: Flask):
    try:
        app.config['DATABASE'] = {
            'dbname': app.config['DB_NAME'],
            'user': app.config['DB_USER'],
            'password': app.config['DB_PASSWORD'],
            'host': app.config['DB_HOST'],
            'port': app.config['DB_PORT']
        }
        logger.debug("Database configuration initialized.")
    except KeyError as e:
        logger.error(f"Missing database configuration: {e}")
        raise


def get_db_connection(app: Flask):
    db_config = app.config['DATABASE']
    try:
        conn = psycopg2.connect(**db_config)
        logger.debug("Database connection established.")
        return conn
    except psycopg2.DatabaseError as e:
        logger.error(f"Database connection error: {e}")
        raise
