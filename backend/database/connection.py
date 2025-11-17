"""
Database connection utility for MySQL.
Provides connection pooling and helper functions.
"""
import os
import logging
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def get_db_connection():
    """
    Get a MySQL database connection.
    
    Returns:
        pymysql.Connection: Database connection object
    """
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'airzone_user'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'airzone'),
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=False
        )
        return connection
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise


def get_db_cursor(connection=None):
    """
    Get a database cursor.
    
    Args:
        connection: Existing connection or None to create new one
        
    Returns:
        tuple: (connection, cursor)
    """
    if connection is None:
        connection = get_db_connection()
    
    cursor = connection.cursor()
    return connection, cursor


def close_db_connection(connection, cursor=None):
    """
    Close database connection and cursor.
    
    Args:
        connection: Database connection
        cursor: Database cursor (optional)
    """
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    except Exception as e:
        logger.error(f"Error closing database connection: {str(e)}")
