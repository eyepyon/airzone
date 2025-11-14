"""Structured logging configuration for the Airzone application"""

import logging
import logging.handlers
import json
import os
from datetime import datetime
from typing import Any, Dict


class StructuredFormatter(logging.Formatter):
    """Custom formatter that outputs structured JSON logs"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data: Dict[str, Any] = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add extra fields if present
        if hasattr(record, 'request_path'):
            log_data['request_path'] = record.request_path
        if hasattr(record, 'request_method'):
            log_data['request_method'] = record.request_method
        if hasattr(record, 'user_agent'):
            log_data['user_agent'] = record.user_agent
        if hasattr(record, 'ip_address'):
            log_data['ip_address'] = record.ip_address
        if hasattr(record, 'error_type'):
            log_data['error_type'] = record.error_type
        if hasattr(record, 'error_code'):
            log_data['error_code'] = record.error_code
        if hasattr(record, 'error_details'):
            log_data['error_details'] = record.error_details
        if hasattr(record, 'traceback'):
            log_data['traceback'] = record.traceback
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


class SimpleFormatter(logging.Formatter):
    """Simple human-readable formatter for development"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as human-readable text"""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        level = record.levelname
        logger_name = record.name
        message = record.getMessage()
        
        log_line = f"[{timestamp}] {level:8s} {logger_name}: {message}"
        
        # Add extra context if available
        if hasattr(record, 'request_path'):
            log_line += f" | path={record.request_path}"
        if hasattr(record, 'request_method'):
            log_line += f" method={record.request_method}"
        
        # Add exception info if present
        if record.exc_info:
            log_line += "\n" + self.formatException(record.exc_info)
        
        return log_line


def setup_logging(app):
    """Configure structured logging for the application"""
    
    # Get log level from environment or config
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_format = os.getenv('LOG_FORMAT', 'simple')  # 'simple' or 'json'
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    root_logger.handlers = []
    
    # Choose formatter based on environment
    if log_format == 'json' or app.config.get('ENV') == 'production':
        formatter = StructuredFormatter()
    else:
        formatter = SimpleFormatter()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler for all logs
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'airzone.log'),
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # File handler for errors only
    error_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'airzone_errors.log'),
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)
    
    # Configure Flask app logger
    app.logger.setLevel(log_level)
    
    # Log startup message
    app.logger.info(
        f"Logging configured",
        extra={
            'log_level': log_level,
            'log_format': log_format,
            'environment': app.config.get('ENV', 'development')
        }
    )
    
    # Suppress noisy loggers
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name"""
    return logging.getLogger(name)
