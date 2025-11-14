"""Rate limiting middleware for API endpoints"""

import time
import logging
from typing import Dict, Optional
from functools import wraps
from flask import request, g
from collections import defaultdict
from threading import Lock
from exceptions import RateLimitExceededError

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple in-memory rate limiter using token bucket algorithm"""
    
    def __init__(self):
        self.buckets: Dict[str, Dict] = defaultdict(lambda: {
            'tokens': 0,
            'last_update': time.time()
        })
        self.lock = Lock()
    
    def is_allowed(
        self,
        key: str,
        max_requests: int,
        window_seconds: int
    ) -> tuple[bool, Optional[int]]:
        """
        Check if request is allowed based on rate limit
        
        Args:
            key: Unique identifier for the client (e.g., IP address or user ID)
            max_requests: Maximum number of requests allowed
            window_seconds: Time window in seconds
        
        Returns:
            Tuple of (is_allowed, retry_after_seconds)
        """
        with self.lock:
            bucket = self.buckets[key]
            current_time = time.time()
            
            # Calculate time elapsed since last update
            time_elapsed = current_time - bucket['last_update']
            
            # Refill tokens based on time elapsed
            refill_rate = max_requests / window_seconds
            bucket['tokens'] = min(
                max_requests,
                bucket['tokens'] + (time_elapsed * refill_rate)
            )
            bucket['last_update'] = current_time
            
            # Check if we have tokens available
            if bucket['tokens'] >= 1:
                bucket['tokens'] -= 1
                return True, None
            else:
                # Calculate retry after time
                tokens_needed = 1 - bucket['tokens']
                retry_after = int(tokens_needed / refill_rate)
                return False, retry_after
    
    def reset(self, key: str):
        """Reset rate limit for a specific key"""
        with self.lock:
            if key in self.buckets:
                del self.buckets[key]
    
    def cleanup_old_entries(self, max_age_seconds: int = 3600):
        """Remove old entries to prevent memory leak"""
        with self.lock:
            current_time = time.time()
            keys_to_remove = [
                key for key, bucket in self.buckets.items()
                if current_time - bucket['last_update'] > max_age_seconds
            ]
            for key in keys_to_remove:
                del self.buckets[key]


# Global rate limiter instance
rate_limiter = RateLimiter()


def get_client_identifier() -> str:
    """Get unique identifier for the client"""
    # Try to get user ID from JWT if authenticated
    if hasattr(g, 'current_user') and g.current_user:
        return f"user:{g.current_user.id}"
    
    # Fall back to IP address
    # Check for X-Forwarded-For header (for proxies)
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        # Get the first IP in the chain
        ip = forwarded_for.split(',')[0].strip()
    else:
        ip = request.remote_addr
    
    return f"ip:{ip}"


def rate_limit(max_requests: int = 100, window_seconds: int = 3600):
    """
    Decorator to apply rate limiting to a route
    
    Args:
        max_requests: Maximum number of requests allowed
        window_seconds: Time window in seconds (default: 1 hour)
    
    Example:
        @rate_limit(max_requests=10, window_seconds=60)  # 10 requests per minute
        def my_route():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client identifier
            client_id = get_client_identifier()
            
            # Create rate limit key
            rate_limit_key = f"{request.endpoint}:{client_id}"
            
            # Check rate limit
            is_allowed, retry_after = rate_limiter.is_allowed(
                rate_limit_key,
                max_requests,
                window_seconds
            )
            
            if not is_allowed:
                logger.warning(
                    f"Rate limit exceeded",
                    extra={
                        'client_id': client_id,
                        'endpoint': request.endpoint,
                        'request_path': request.path,
                        'retry_after': retry_after
                    }
                )
                raise RateLimitExceededError(
                    message=f"Rate limit exceeded. Try again in {retry_after} seconds.",
                    retry_after=retry_after
                )
            
            # Add rate limit info to response headers
            response = f(*args, **kwargs)
            
            # If response is a tuple (response, status_code), handle it
            if isinstance(response, tuple):
                response_obj, status_code = response[0], response[1]
            else:
                response_obj = response
                status_code = 200
            
            # Add rate limit headers if response is a Flask response object
            if hasattr(response_obj, 'headers'):
                response_obj.headers['X-RateLimit-Limit'] = str(max_requests)
                response_obj.headers['X-RateLimit-Window'] = str(window_seconds)
            
            return response
        
        return decorated_function
    return decorator


def global_rate_limit(max_requests: int = 1000, window_seconds: int = 3600):
    """
    Apply global rate limit to all requests from a client
    
    Args:
        max_requests: Maximum number of requests allowed globally
        window_seconds: Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get client identifier
            client_id = get_client_identifier()
            
            # Create global rate limit key
            rate_limit_key = f"global:{client_id}"
            
            # Check rate limit
            is_allowed, retry_after = rate_limiter.is_allowed(
                rate_limit_key,
                max_requests,
                window_seconds
            )
            
            if not is_allowed:
                logger.warning(
                    f"Global rate limit exceeded",
                    extra={
                        'client_id': client_id,
                        'request_path': request.path,
                        'retry_after': retry_after
                    }
                )
                raise RateLimitExceededError(
                    message=f"Too many requests. Try again in {retry_after} seconds.",
                    retry_after=retry_after
                )
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def setup_rate_limiting(app):
    """Setup global rate limiting for the application"""
    
    # Apply global rate limit to all requests
    @app.before_request
    def check_global_rate_limit():
        """Check global rate limit before processing request"""
        # Skip rate limiting for health check and static files
        if request.path in ['/health', '/favicon.ico']:
            return
        
        # Get client identifier
        client_id = get_client_identifier()
        
        # Create global rate limit key
        rate_limit_key = f"global:{client_id}"
        
        # Check rate limit (1000 requests per hour by default)
        max_requests = app.config.get('RATELIMIT_DEFAULT_LIMIT', 1000)
        window_seconds = app.config.get('RATELIMIT_DEFAULT_WINDOW', 3600)
        
        is_allowed, retry_after = rate_limiter.is_allowed(
            rate_limit_key,
            max_requests,
            window_seconds
        )
        
        if not is_allowed:
            logger.warning(
                f"Global rate limit exceeded",
                extra={
                    'client_id': client_id,
                    'request_path': request.path,
                    'retry_after': retry_after
                }
            )
            raise RateLimitExceededError(
                message=f"Too many requests. Try again in {retry_after} seconds.",
                retry_after=retry_after
            )
    
    # Cleanup old entries periodically
    import atexit
    
    def cleanup():
        rate_limiter.cleanup_old_entries()
    
    atexit.register(cleanup)
    
    logger.info("Rate limiting configured")
