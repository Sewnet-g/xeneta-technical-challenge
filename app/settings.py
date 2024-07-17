import os

from dotenv import load_dotenv

load_dotenv()
# Flask configuration
FLASK_DEBUG = os.getenv('DEBUG', False)

# Database configuration
DB_NAME = os.getenv('DB_NAME', '')
DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', '')  # This should match the service name in docker-compose.yml
DB_PORT = int(os.getenv('DB_PORT', 5432))

# Logging configuration
LOGGING_CONFIG = 'logging.json'
