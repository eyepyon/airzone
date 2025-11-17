"""
JWT Authentication Middleware for Airzone API.
Provides JWT token verification, authentication decorators, and user context helpers.

Requirements: 6.1, 6.7
"""
from functools import wraps
from typing import Optional, Dict, Callable
from flask import request, jsonify, g, current_app
import jwt
import logging

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Custom exception for authentication errors"""
    pass


def extract_token_from_header() -> Optional[str]:
    """
    Extract JWT token from Authorization header.
    
    Returns:
        Optional[str]: JWT token or None if not found
        
    Requirements: 6.1 - JWT Bearer Token authentication
    """
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header:
        return None
    
    # Expected format: "Bearer <token>"
    parts = auth_header.split()
    
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        logger.warning(f"Invalid Authorization header format: {auth_header[:20]}...")
        return None
    
    return parts[1]


def verify_jwt_token(token: str) -> Dict:
    """
    Verify JWT token and extract payload.
    
    Args:
        token: JWT token string
        
    Returns:
        Dict: Token payload containing user_id and other claims
        
    Raises:
        AuthenticationError: If token is invalid or expired
        
    Requirements: 6.1 - JWT token verification
    """
    try:
        # Get JWT secret from app config
        jwt_secret = current_app.config.get('JWT_SECRET_KEY')
        
        if not jwt_secret:
            logger.error("JWT_SECRET_KEY not configured")
            raise AuthenticationError("Authentication configuration error")
        
        # Decode and verify token
        payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        
        # Verify token type is 'access'
        if payload.get('type') != 'access':
            logger.warning(f"Invalid token type: {payload.get('type')}")
            raise AuthenticationError("Invalid token type")
        
        # Verify required fields
        if 'user_id' not in payload:
            logger.warning("Token missing user_id claim")
            raise AuthenticationError("Invalid token payload")
        
        logger.debug(f"Successfully verified token for user: {payload['user_id']}")
        return payload
        
    except jwt.ExpiredSignatureError:
        logger.info("Token has expired")
        raise AuthenticationError("Token has expired")
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {str(e)}")
        raise AuthenticationError("Invalid token")
    except Exception as e:
        logger.error(f"Unexpected error verifying token: {str(e)}")
        raise AuthenticationError("Token verification failed")


def get_current_user() -> Optional[Dict]:
    """
    Get current authenticated user from request context.
    
    This helper function retrieves the user information that was set by the
    jwt_required decorator. It should be called within a request context
    after authentication has been performed.
    
    Returns:
        Optional[Dict]: User information dictionary or None if not authenticated
        
    Example:
        @jwt_required
        def protected_route():
            user = get_current_user()
            return jsonify({'user_id': user['user_id']})
            
    Requirements: 6.1 - User authentication verification
    """
    return g.get('current_user', None)


def get_current_user_id() -> Optional[str]:
    """
    Get current authenticated user ID from request context.
    
    Convenience function to get just the user_id without the full user dict.
    
    Returns:
        Optional[str]: User ID or None if not authenticated
    """
    user = get_current_user()
    return user.get('user_id') if user else None


def jwt_required(f: Callable) -> Callable:
    """
    Decorator to protect routes with JWT authentication.
    
    This decorator verifies the JWT token from the Authorization header
    and sets the current user in the Flask g object. If authentication fails,
    it returns a 401 Unauthorized response.
    
    Usage:
        @app.route('/protected')
        @jwt_required
        def protected_route():
            user = get_current_user()
            return jsonify({'message': f'Hello {user["user_id"]}'})
    
    Args:
        f: The route function to protect
        
    Returns:
        Callable: Wrapped function with authentication
        
    Requirements:
        - 6.1: JWT Bearer Token authentication for all API endpoints
        - 6.7: API authentication and authorization
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Extract token from Authorization header
            token = extract_token_from_header()
            
            if not token:
                logger.info(f"Missing token for {request.method} {request.path}")
                return jsonify({
                    'status': 'error',
                    'error': 'Authorization token is missing',
                    'code': 401
                }), 401
            
            # Verify token and extract payload
            payload = verify_jwt_token(token)
            
            # Store user info in Flask g object for access in route handlers
            g.current_user = {
                'user_id': payload['user_id'],
                'token_type': payload.get('type'),
                'issued_at': payload.get('iat'),
                'expires_at': payload.get('exp')
            }
            
            logger.info(
                f"Authenticated request: {request.method} {request.path}",
                extra={
                    'user_id': payload['user_id'],
                    'endpoint': request.endpoint
                }
            )
            
            # Call the actual route function
            return f(*args, **kwargs)
            
        except AuthenticationError as e:
            logger.warning(
                f"Authentication failed for {request.method} {request.path}: {str(e)}",
                extra={
                    'error': str(e),
                    'ip_address': request.remote_addr
                }
            )
            return jsonify({
                'status': 'error',
                'error': str(e),
                'code': 401
            }), 401
        except Exception as e:
            logger.error(
                f"Unexpected error in authentication: {str(e)}",
                extra={
                    'error': str(e),
                    'endpoint': request.endpoint
                }
            )
            return jsonify({
                'status': 'error',
                'error': 'Authentication failed',
                'code': 401
            }), 401
    
    return decorated_function


def jwt_optional(f: Callable) -> Callable:
    """
    Decorator for routes where authentication is optional.
    
    Similar to jwt_required but doesn't return 401 if token is missing.
    If a valid token is provided, user info is set in g.current_user.
    
    Usage:
        @app.route('/public-or-private')
        @jwt_optional
        def mixed_route():
            user = get_current_user()
            if user:
                return jsonify({'message': 'Authenticated user'})
            return jsonify({'message': 'Anonymous user'})
    
    Args:
        f: The route function to wrap
        
    Returns:
        Callable: Wrapped function with optional authentication
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Extract token from Authorization header
            token = extract_token_from_header()
            
            if token:
                # Verify token and extract payload
                payload = verify_jwt_token(token)
                
                # Store user info in Flask g object
                g.current_user = {
                    'user_id': payload['user_id'],
                    'token_type': payload.get('type'),
                    'issued_at': payload.get('iat'),
                    'expires_at': payload.get('exp')
                }
                
                logger.debug(f"Optional auth: User {payload['user_id']} authenticated")
            else:
                # No token provided, continue as anonymous
                g.current_user = None
                logger.debug("Optional auth: No token provided, continuing as anonymous")
            
        except AuthenticationError as e:
            # Invalid token provided, but we don't fail the request
            logger.info(f"Optional auth: Invalid token provided: {str(e)}")
            g.current_user = None
        except Exception as e:
            logger.warning(f"Optional auth: Unexpected error: {str(e)}")
            g.current_user = None
        
        # Always call the route function
        return f(*args, **kwargs)
    
    return decorated_function


def require_role(role: str) -> Callable:
    """
    Decorator to require specific user role (for future role-based access control).
    
    This is a placeholder for future RBAC implementation.
    Currently, it just ensures the user is authenticated.
    
    Usage:
        @app.route('/admin')
        @require_role('admin')
        def admin_route():
            return jsonify({'message': 'Admin access'})
    
    Args:
        role: Required role name
        
    Returns:
        Callable: Decorator function
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        @jwt_required
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            
            # TODO: Implement role checking when user roles are added to the system
            # For now, just ensure user is authenticated (done by jwt_required)
            
            logger.info(
                f"Role check (placeholder): user {user['user_id']} accessing {request.endpoint}",
                extra={'required_role': role}
            )
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator


def require_admin(f: Callable) -> Callable:
    """
    Decorator to require admin privileges.
    
    This decorator ensures the user is authenticated and has admin privileges.
    Currently checks if user has 'is_admin' flag in the database.
    
    Usage:
        @app.route('/admin/users')
        @require_admin
        def admin_users(current_user):
            return jsonify({'users': get_all_users()})
    
    Args:
        f: The route function to protect
        
    Returns:
        Callable: Wrapped function with admin authentication
    """
    @wraps(f)
    @jwt_required
    def decorated_function(*args, **kwargs):
        from database.connection import get_db_connection
        
        user = get_current_user()
        user_id = user['user_id']
        
        try:
            # Check if user is admin
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT is_admin FROM users WHERE id = %s",
                (user_id,)
            )
            user_data = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if not user_data or not user_data.get('is_admin'):
                logger.warning(
                    f"Admin access denied for user {user_id} to {request.endpoint}"
                )
                return jsonify({
                    'status': 'error',
                    'error': 'Admin privileges required',
                    'code': 403
                }), 403
            
            logger.info(
                f"Admin access granted: user {user_id} accessing {request.endpoint}"
            )
            
            # Pass current_user to the route function
            return f(user, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"Error checking admin privileges: {str(e)}")
            return jsonify({
                'status': 'error',
                'error': 'Authorization check failed',
                'code': 500
            }), 500
    
    return decorated_function
