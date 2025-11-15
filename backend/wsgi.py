"""
WSGI Entry Point for Apache mod_wsgi

This file is used by Apache's mod_wsgi to serve the Flask application.
It loads the application and makes it available to the WSGI server.

Apache Configuration:
    WSGIScriptAlias /api /var/www/airzone/backend/wsgi.py
    WSGIDaemonProcess airzone_backend python-home=/var/www/airzone/backend/venv
    WSGIProcessGroup airzone_backend
"""

import sys
import os
import logging
from dotenv import load_dotenv

# Add the application directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

# Set up logging for WSGI errors
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('/var/log/airzone/wsgi.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

try:
    # Import the Flask application
    from app import app as application
    
    logger.info("WSGI application loaded successfully")
    
except Exception as e:
    logger.error(f"Failed to load WSGI application: {str(e)}", exc_info=True)
    raise

# For debugging: print environment info
if application.debug:
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Python path: {sys.path}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Environment: {application.config.get('ENV')}")
