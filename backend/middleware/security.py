"""Security middleware for input validation, sanitization, and protection"""

import re
import html
import logging
from typing import Any, Dict, Optional, List
from functools import wraps
from flask import request, jsonify, g
from werkzeug.datastructures import ImmutableMultiDict
from exceptions import ValidationError, RateLimitExceededError

logger = logging.getLogger(__name__)


class InputValidator:
    """Validator for input data with sanitization"""
    
    # Common regex patterns
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    ALPHANUMERIC_PATTERN = re.compile(r'^[a-zA-Z0-9]+$')
    URL_PATTERN = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    
    # Dangerous patterns for XSS detection
    XSS_PATTERNS = [
        re.compile(r'<script[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL),
        re.compile(r'javascript:', re.IGNORECASE),
        re.compile(r'on\w+\s*=', re.IGNORECASE),  # Event handlers like onclick=
        re.compile(r'<iframe[^>]*>', re.IGNORECASE),
        re.compile(r'<object[^>]*>', re.IGNORECASE),
        re.compile(r'<embed[^>]*>', re.IGNORECASE),
    ]
    
    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        re.compile(r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)\b)", re.IGNORECASE),
        re.compile(r"(--|;|\/\*|\*\/|xp_|sp_)", re.IGNORECASE),
        re.compile(r"(\bOR\b.*=.*|1\s*=\s*1)", re.IGNORECASE),
    ]
    
    @staticmethod
    def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
        """Sanitize string input by escaping HTML and removing dangerous characters"""
        if not isinstance(value, str):
            raise ValidationError("Value must be a string")
        
        # Remove null bytes
        value = value.replace('\x00', '')
        
        # Escape HTML entities
        value = html.escape(value)
        
        # Trim whitespace
        value = value.strip()
        
        # Check max length
        if max_length and len(value) > max_length:
            raise ValidationError(f"String exceeds maximum length of {max_length}")
        
        return value
    
    @staticmethod
    def validate_email(email: str) -> str:
        """Validate and sanitize email address"""
        email = InputValidator.sanitize_string(email, max_length=255)
        
        if not InputValidator.EMAIL_PATTERN.match(email):
            raise ValidationError("Invalid email format", field="email")
        
        return email.lower()
    
    @staticmethod
    def validate_uuid(uuid_str: str) -> str:
        """Validate UUID format"""
        uuid_str = uuid_str.strip()
        
        if not InputValidator.UUID_PATTERN.match(uuid_str):
            raise ValidationError("Invalid UUID format", field="id")
        
        return uuid_str.lower()
    
    @staticmethod
    def validate_url(url: str) -> str:
        """Validate URL format"""
        url = url.strip()
        
        if not InputValidator.URL_PATTERN.match(url):
            raise ValidationError("Invalid URL format", field="url")
        
        return url
    
    @staticmethod
    def validate_integer(value: Any, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
        """Validate integer value with optional range"""
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            raise ValidationError("Value must be an integer")
        
        if min_value is not None and int_value < min_value:
            raise ValidationError(f"Value must be at least {min_value}")
        
        if max_value is not None and int_value > max_value:
            raise ValidationError(f"Value must be at most {max_value}")
        
        return int_value
    
    @staticmethod
    def validate_positive_integer(value: Any) -> int:
        """Validate positive integer"""
        return InputValidator.validate_integer(value, min_value=1)
    
    @staticmethod
    def check_xss(value: str) -> None:
        """Check for XSS attack patterns"""
        for pattern in InputValidator.XSS_PATTERNS:
            if pattern.search(value):
                logger.warning(
                    f"XSS attempt detected",
                    extra={
                        'value': value[:100],  # Log first 100 chars
                        'ip_address': request.remote_addr
                    }
                )
                raise ValidationError("Invalid input detected")
    
    @staticmethod
    def check_sql_injection(value: str) -> None:
        """Check for SQL injection patterns"""
        for pattern in InputValidator.SQL_INJECTION_PATTERNS:
            if pattern.search(value):
                logger.warning(
                    f"SQL injection attempt detected",
                    extra={
                        'value': value[:100],  # Log first 100 chars
                        'ip_address': request.remote_addr
                    }
                )
                raise ValidationError("Invalid input detected")
    
    @staticmethod
    def sanitize_dict(data: Dict[str, Any], allowed_keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """Sanitize dictionary by removing dangerous values and checking allowed keys"""
        if not isinstance(data, dict):
            raise ValidationError("Data must be a dictionary")
        
        # Check for allowed keys if specified
        if allowed_keys:
            invalid_keys = set(data.keys()) - set(allowed_keys)
            if invalid_keys:
                raise ValidationError(f"Invalid keys: {', '.join(invalid_keys)}")
        
        sanitized = {}
        for key, value in data.items():
            # Sanitize key
            key = InputValidator.sanitize_string(str(key), max_length=100)
            
            # Sanitize value based on type
            if isinstance(value, str):
                # Check for XSS and SQL injection
                InputValidator.check_xss(value)
                InputValidator.check_sql_injection(value)
                sanitized[key] = InputValidator.sanitize_string(value)
            elif isinstance(value, (int, float, bool)):
                sanitized[key] = value
            elif isinstance(value, dict):
                sanitized[key] = InputValidator.sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    InputValidator.sanitize_string(str(item)) if isinstance(item, str) else item
                    for item in value
                ]
            elif value is None:
                sanitized[key] = None
            else:
                # Convert other types to string and sanitize
                sanitized[key] = InputValidator.sanitize_string(str(value))
        
        return sanitized


class CSRFProtection:
    """CSRF protection middleware"""
    
    # Methods that require CSRF protection
    PROTECTED_METHODS = ['POST', 'PUT', 'DELETE', 'PATCH']
    
    # Paths that are exempt from CSRF protection
    EXEMPT_PATHS = [
        '/api/v1/payments/webhook',  # Stripe webhook
        '/health',
    ]
    
    @staticmethod
    def generate_csrf_token() -> str:
        """Generate a CSRF token"""
        import secrets
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def verify_csrf_token(token: str) -> bool:
        """Verify CSRF token"""
        # Get token from session or database
        stored_token = g.get('csrf_token')
        
        if not stored_token:
            return False
        
        # Constant-time comparison to prevent timing attacks
        import hmac
        return hmac.compare_digest(token, stored_token)
    
    @staticmethod
    def is_exempt(path: str) -> bool:
        """Check if path is exempt from CSRF protection"""
        return any(path.startswith(exempt) for exempt in CSRFProtection.EXEMPT_PATHS)


def validate_json_request(required_fields: Optional[List[str]] = None, allowed_fields: Optional[List[str]] = None):
    """Decorator to validate JSON request data"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check content type
            if not request.is_json:
                raise ValidationError("Content-Type must be application/json")
            
            # Get JSON data
            try:
                data = request.get_json()
            except Exception as e:
                logger.warning(f"Invalid JSON: {str(e)}")
                raise ValidationError("Invalid JSON format")
            
            if data is None:
                raise ValidationError("Request body is required")
            
            # Check required fields
            if required_fields:
                missing_fields = [field for field in required_fields if field not in data]
                if missing_fields:
                    raise ValidationError(
                        f"Missing required fields: {', '.join(missing_fields)}",
                        details={'missing_fields': missing_fields}
                    )
            
            # Sanitize data
            sanitized_data = InputValidator.sanitize_dict(data, allowed_keys=allowed_fields)
            
            # Replace request data with sanitized version
            request.sanitized_data = sanitized_data
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def csrf_protect():
    """Decorator to enable CSRF protection for a route"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Skip if method doesn't require protection
            if request.method not in CSRFProtection.PROTECTED_METHODS:
                return f(*args, **kwargs)
            
            # Skip if path is exempt
            if CSRFProtection.is_exempt(request.path):
                return f(*args, **kwargs)
            
            # Get CSRF token from header
            csrf_token = request.headers.get('X-CSRF-Token')
            
            if not csrf_token:
                logger.warning(
                    "Missing CSRF token",
                    extra={
                        'request_path': request.path,
                        'ip_address': request.remote_addr
                    }
                )
                raise ValidationError("CSRF token is required")
            
            # Verify token
            if not CSRFProtection.verify_csrf_token(csrf_token):
                logger.warning(
                    "Invalid CSRF token",
                    extra={
                        'request_path': request.path,
                        'ip_address': request.remote_addr
                    }
                )
                raise ValidationError("Invalid CSRF token")
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def sanitize_query_params():
    """Middleware to sanitize query parameters"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Sanitize query parameters
            sanitized_args = {}
            for key, value in request.args.items():
                try:
                    sanitized_key = InputValidator.sanitize_string(key, max_length=100)
                    sanitized_value = InputValidator.sanitize_string(value, max_length=1000)
                    
                    # Check for XSS and SQL injection
                    InputValidator.check_xss(sanitized_value)
                    InputValidator.check_sql_injection(sanitized_value)
                    
                    sanitized_args[sanitized_key] = sanitized_value
                except ValidationError as e:
                    logger.warning(
                        f"Invalid query parameter: {key}={value}",
                        extra={
                            'request_path': request.path,
                            'ip_address': request.remote_addr
                        }
                    )
                    raise e
            
            # Store sanitized args
            request.sanitized_args = sanitized_args
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def setup_security_headers(app):
    """Setup security headers for all responses"""
    
    @app.after_request
    def add_security_headers(response):
        """Add security headers to response"""
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Content Security Policy
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https://api.stripe.com; "
            "frame-ancestors 'none';"
        )
        
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response.headers['Permissions-Policy'] = (
            "geolocation=(), "
            "microphone=(), "
            "camera=(), "
            "payment=(self)"
        )
        
        # HSTS (HTTP Strict Transport Security) - only in production
        if app.config.get('ENV') == 'production':
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response
