"""Global error handlers for the Airzone application"""

import logging
import traceback
from typing import Tuple
from flask import jsonify, request
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from exceptions import (
    AirzoneException,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    ResourceNotFoundError,
    ResourceConflictError,
    RateLimitExceededError,
    ExternalServiceError,
    DatabaseError
)

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """Register all error handlers with the Flask app"""
    
    @app.errorhandler(AirzoneException)
    def handle_airzone_exception(error: AirzoneException) -> Tuple[dict, int]:
        """Handle custom Airzone exceptions"""
        logger.warning(
            f"Airzone exception: {error.message}",
            extra={
                'error_type': error.__class__.__name__,
                'error_code': error.code,
                'error_details': error.details,
                'request_path': request.path,
                'request_method': request.method,
                'user_agent': request.headers.get('User-Agent')
            }
        )
        return jsonify(error.to_dict()), error.code
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError) -> Tuple[dict, int]:
        """Handle validation errors"""
        logger.info(
            f"Validation error: {error.message}",
            extra={
                'error_details': error.details,
                'request_path': request.path,
                'request_method': request.method
            }
        )
        return jsonify(error.to_dict()), error.code
    
    @app.errorhandler(AuthenticationError)
    def handle_authentication_error(error: AuthenticationError) -> Tuple[dict, int]:
        """Handle authentication errors"""
        logger.warning(
            f"Authentication error: {error.message}",
            extra={
                'request_path': request.path,
                'request_method': request.method,
                'ip_address': request.remote_addr
            }
        )
        return jsonify(error.to_dict()), error.code
    
    @app.errorhandler(AuthorizationError)
    def handle_authorization_error(error: AuthorizationError) -> Tuple[dict, int]:
        """Handle authorization errors"""
        logger.warning(
            f"Authorization error: {error.message}",
            extra={
                'request_path': request.path,
                'request_method': request.method,
                'ip_address': request.remote_addr
            }
        )
        return jsonify(error.to_dict()), error.code
    
    @app.errorhandler(ResourceNotFoundError)
    def handle_not_found_error(error: ResourceNotFoundError) -> Tuple[dict, int]:
        """Handle resource not found errors"""
        logger.info(
            f"Resource not found: {error.message}",
            extra={
                'error_details': error.details,
                'request_path': request.path
            }
        )
        return jsonify(error.to_dict()), error.code
    
    @app.errorhandler(ResourceConflictError)
    def handle_conflict_error(error: ResourceConflictError) -> Tuple[dict, int]:
        """Handle resource conflict errors"""
        logger.warning(
            f"Resource conflict: {error.message}",
            extra={
                'error_details': error.details,
                'request_path': request.path
            }
        )
        return jsonify(error.to_dict()), error.code
    
    @app.errorhandler(RateLimitExceededError)
    def handle_rate_limit_error(error: RateLimitExceededError) -> Tuple[dict, int]:
        """Handle rate limit exceeded errors"""
        logger.warning(
            f"Rate limit exceeded",
            extra={
                'ip_address': request.remote_addr,
                'request_path': request.path,
                'request_method': request.method
            }
        )
        return jsonify(error.to_dict()), error.code
    
    @app.errorhandler(ExternalServiceError)
    def handle_external_service_error(error: ExternalServiceError) -> Tuple[dict, int]:
        """Handle external service errors"""
        logger.error(
            f"External service error: {error.message}",
            extra={
                'error_details': error.details,
                'request_path': request.path
            }
        )
        return jsonify(error.to_dict()), error.code
    
    @app.errorhandler(DatabaseError)
    def handle_database_error(error: DatabaseError) -> Tuple[dict, int]:
        """Handle database errors"""
        logger.error(
            f"Database error: {error.message}",
            extra={
                'error_details': error.details,
                'request_path': request.path
            },
            exc_info=True
        )
        return jsonify(error.to_dict()), error.code
    
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error: SQLAlchemyError) -> Tuple[dict, int]:
        """Handle SQLAlchemy database errors"""
        logger.error(
            f"SQLAlchemy error: {str(error)}",
            extra={
                'request_path': request.path,
                'request_method': request.method
            },
            exc_info=True
        )
        
        # Check for specific error types
        if isinstance(error, IntegrityError):
            return jsonify({
                'status': 'error',
                'error': 'Database integrity constraint violation',
                'code': 409
            }), 409
        
        return jsonify({
            'status': 'error',
            'error': 'Database error occurred',
            'code': 500
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException) -> Tuple[dict, int]:
        """Handle Werkzeug HTTP exceptions"""
        logger.warning(
            f"HTTP exception: {error.code} - {error.description}",
            extra={
                'request_path': request.path,
                'request_method': request.method,
                'status_code': error.code
            }
        )
        return jsonify({
            'status': 'error',
            'error': error.description or 'HTTP error',
            'code': error.code
        }), error.code
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception) -> Tuple[dict, int]:
        """Handle unexpected errors"""
        logger.error(
            f"Unexpected error: {str(error)}",
            extra={
                'error_type': error.__class__.__name__,
                'request_path': request.path,
                'request_method': request.method,
                'traceback': traceback.format_exc()
            },
            exc_info=True
        )
        
        # Don't expose internal error details in production
        return jsonify({
            'status': 'error',
            'error': 'An unexpected error occurred',
            'code': 500
        }), 500
    
    @app.errorhandler(400)
    def handle_400(error) -> Tuple[dict, int]:
        """Handle 400 Bad Request"""
        return jsonify({
            'status': 'error',
            'error': 'Bad request',
            'code': 400
        }), 400
    
    @app.errorhandler(401)
    def handle_401(error) -> Tuple[dict, int]:
        """Handle 401 Unauthorized"""
        return jsonify({
            'status': 'error',
            'error': 'Unauthorized',
            'code': 401
        }), 401
    
    @app.errorhandler(403)
    def handle_403(error) -> Tuple[dict, int]:
        """Handle 403 Forbidden"""
        return jsonify({
            'status': 'error',
            'error': 'Forbidden',
            'code': 403
        }), 403
    
    @app.errorhandler(404)
    def handle_404(error) -> Tuple[dict, int]:
        """Handle 404 Not Found"""
        return jsonify({
            'status': 'error',
            'error': 'Resource not found',
            'code': 404
        }), 404
    
    @app.errorhandler(405)
    def handle_405(error) -> Tuple[dict, int]:
        """Handle 405 Method Not Allowed"""
        return jsonify({
            'status': 'error',
            'error': 'Method not allowed',
            'code': 405
        }), 405
    
    @app.errorhandler(409)
    def handle_409(error) -> Tuple[dict, int]:
        """Handle 409 Conflict"""
        return jsonify({
            'status': 'error',
            'error': 'Resource conflict',
            'code': 409
        }), 409
    
    @app.errorhandler(429)
    def handle_429(error) -> Tuple[dict, int]:
        """Handle 429 Too Many Requests"""
        return jsonify({
            'status': 'error',
            'error': 'Rate limit exceeded',
            'code': 429
        }), 429
    
    @app.errorhandler(500)
    def handle_500(error) -> Tuple[dict, int]:
        """Handle 500 Internal Server Error"""
        logger.error(
            f"Internal server error",
            extra={
                'request_path': request.path,
                'request_method': request.method
            },
            exc_info=True
        )
        return jsonify({
            'status': 'error',
            'error': 'Internal server error',
            'code': 500
        }), 500
    
    @app.errorhandler(502)
    def handle_502(error) -> Tuple[dict, int]:
        """Handle 502 Bad Gateway"""
        return jsonify({
            'status': 'error',
            'error': 'Bad gateway - external service error',
            'code': 502
        }), 502
    
    @app.errorhandler(503)
    def handle_503(error) -> Tuple[dict, int]:
        """Handle 503 Service Unavailable"""
        return jsonify({
            'status': 'error',
            'error': 'Service temporarily unavailable',
            'code': 503
        }), 503
