# Security and Error Handling Implementation

## Overview

Task 7 "エラーハンドリングとセキュリティの実装" has been successfully completed. This document summarizes the implemented security features and error handling mechanisms.

## Implemented Components

### 1. Custom Exception Classes (backend/exceptions.py)

Comprehensive exception hierarchy for the Airzone application:

#### Base Exception
- `AirzoneException` - Base class with standardized error response format

#### Client Errors (4xx)
- `ValidationError` (400) - Input validation failures
- `AuthenticationError` (401) - Authentication failures
- `AuthorizationError` (403) - Authorization/permission failures
- `ResourceNotFoundError` (404) - Resource not found
- `ResourceConflictError` (409) - Resource conflicts (e.g., stock issues)
- `RateLimitExceededError` (429) - Rate limit exceeded

#### Server Errors (5xx)
- `ExternalServiceError` (502) - External API failures
- `DatabaseError` (500) - Database operation failures

#### Domain-Specific Exceptions
- `InsufficientStockError` - Product stock insufficient
- `NFTRequirementError` - NFT ownership requirement not met
- `PaymentError` - Payment processing failures
- `BlockchainError` - Blockchain operation failures

### 2. Global Error Handlers (backend/error_handlers.py)

Centralized error handling with structured logging:

- Custom exception handlers for all Airzone exceptions
- SQLAlchemy error handlers
- HTTP exception handlers (400, 401, 403, 404, 405, 409, 429, 500, 502, 503)
- Werkzeug HTTP exception handler
- Catch-all handler for unexpected errors
- Structured logging with request context

### 3. Structured Logging (backend/logging_config.py)

Production-ready logging configuration:

- **StructuredFormatter** - JSON-formatted logs for production
- **SimpleFormatter** - Human-readable logs for development
- **Log Rotation** - Automatic log file rotation (10MB max, 5 backups)
- **Multiple Handlers**:
  - Console handler for real-time monitoring
  - File handler for all logs (airzone.log)
  - Error-only file handler (airzone_errors.log)
- **Contextual Logging** - Request path, method, IP, user agent, etc.

### 4. Input Validation and Sanitization (backend/middleware/security.py)

Comprehensive input validation and sanitization:

#### InputValidator Class
- **Email validation** - RFC-compliant email format validation
- **UUID validation** - UUID v4 format validation
- **URL validation** - HTTP/HTTPS URL validation
- **Integer validation** - Range validation for numeric inputs
- **String sanitization** - HTML escaping, null byte removal, whitespace trimming
- **XSS detection** - Pattern matching for common XSS attacks
- **SQL injection detection** - Pattern matching for SQL injection attempts
- **Dictionary sanitization** - Recursive sanitization with allowed key filtering

#### Decorators
- `@validate_json_request` - Validate and sanitize JSON request bodies
- `@sanitize_query_params` - Sanitize URL query parameters
- `@csrf_protect` - Enable CSRF protection for routes

### 5. CSRF Protection (backend/middleware/security.py)

Cross-Site Request Forgery protection:

- **Token generation** - Cryptographically secure token generation
- **Token verification** - Constant-time comparison to prevent timing attacks
- **Exempt paths** - Configurable paths exempt from CSRF (e.g., webhooks)
- **Protected methods** - POST, PUT, DELETE, PATCH require CSRF tokens
- **Header-based** - CSRF token passed via X-CSRF-Token header

### 6. Security Headers (backend/middleware/security.py)

HTTP security headers automatically added to all responses:

- `X-Frame-Options: DENY` - Prevent clickjacking
- `X-Content-Type-Options: nosniff` - Prevent MIME sniffing
- `X-XSS-Protection: 1; mode=block` - Enable browser XSS protection
- `Content-Security-Policy` - Restrict resource loading
- `Referrer-Policy: strict-origin-when-cross-origin` - Control referrer information
- `Permissions-Policy` - Restrict browser features
- `Strict-Transport-Security` - HSTS (production only)

### 7. Rate Limiting (backend/middleware/rate_limit.py)

Token bucket algorithm for rate limiting:

#### RateLimiter Class
- **Token bucket algorithm** - Smooth rate limiting with burst support
- **Per-client tracking** - Rate limits per IP or authenticated user
- **Configurable limits** - Customizable request limits and time windows
- **Automatic cleanup** - Prevents memory leaks from old entries

#### Decorators
- `@rate_limit(max_requests, window_seconds)` - Per-endpoint rate limiting
- `@global_rate_limit(max_requests, window_seconds)` - Global rate limiting

#### Features
- **Client identification** - IP-based or user-based tracking
- **Retry-After header** - Informs clients when to retry
- **Rate limit headers** - X-RateLimit-Limit, X-RateLimit-Window
- **Structured logging** - Log rate limit violations with context

## Requirements Coverage

### Requirement 6.4: SQL Injection Prevention ✓
- Parameterized queries enforced through SQLAlchemy ORM
- SQL injection pattern detection in input validation
- Structured logging of SQL injection attempts

### Requirement 6.5: XSS Attack Prevention ✓
- HTML entity escaping for all user inputs
- XSS pattern detection (script tags, event handlers, iframes)
- Content Security Policy headers
- Structured logging of XSS attempts

### Requirement 6.6: CSRF Protection ✓
- CSRF token generation and verification
- Protected HTTP methods (POST, PUT, DELETE, PATCH)
- Exempt paths for webhooks
- X-CSRF-Token header validation

### Requirement 6.7: API Rate Limiting ✓
- Token bucket rate limiting algorithm
- Per-client and per-endpoint limits
- Global rate limiting (1000 requests/hour default)
- Rate limit exceeded error responses

### Requirement 6.8: HSTS ✓
- Strict-Transport-Security header in production
- max-age=31536000 (1 year)
- includeSubDomains directive

### Requirement 8.7: Error Response Format ✓
- Standardized JSON error responses
- Consistent format: `{"status": "error", "error": "message", "code": number}`
- Optional details field for additional context
- Structured logging of all errors

## Integration

All security features are integrated into the Flask application (backend/app.py):

```python
# Security headers
setup_security_headers(app)

# Rate limiting
setup_rate_limiting(app)

# Error handlers
register_error_handlers(app)

# Structured logging
setup_logging(app)
```

## Usage Examples

### Using Custom Exceptions
```python
from exceptions import ValidationError, ResourceNotFoundError

# Raise validation error
if not email:
    raise ValidationError("Email is required", field="email")

# Raise not found error
user = user_repo.find_by_id(user_id)
if not user:
    raise ResourceNotFoundError("User", user_id)
```

### Using Input Validation
```python
from middleware.security import InputValidator, validate_json_request

# Validate email
email = InputValidator.validate_email(request.json['email'])

# Validate UUID
user_id = InputValidator.validate_uuid(request.args['user_id'])

# Use decorator for automatic validation
@validate_json_request(required_fields=['email', 'name'])
def create_user():
    data = request.sanitized_data  # Already sanitized
    # ... create user
```

### Using Rate Limiting
```python
from middleware.rate_limit import rate_limit

# Apply rate limit to endpoint
@rate_limit(max_requests=10, window_seconds=60)  # 10 requests per minute
def sensitive_endpoint():
    # ... endpoint logic
```

### Using CSRF Protection
```python
from middleware.security import csrf_protect

# Protect endpoint with CSRF
@csrf_protect()
def create_order():
    # ... order creation logic
```

## Testing

Run the verification script to test all security features:

```bash
cd backend
python verify_security.py
```

The script tests:
- Custom exception classes
- Input validation (email, UUID, integer)
- XSS protection
- SQL injection protection
- String sanitization
- CSRF protection
- Dictionary sanitization

## Security Best Practices

1. **Always validate and sanitize user input** - Use InputValidator for all user-provided data
2. **Use parameterized queries** - SQLAlchemy ORM handles this automatically
3. **Apply rate limiting** - Protect sensitive endpoints with appropriate limits
4. **Enable CSRF protection** - Use @csrf_protect() for state-changing operations
5. **Log security events** - All security violations are logged with context
6. **Use HTTPS in production** - HSTS header enforces secure connections
7. **Keep dependencies updated** - Regularly update security-related packages

## Monitoring and Logging

All security events are logged with structured context:

- **XSS attempts** - Logged with IP address and attempted payload
- **SQL injection attempts** - Logged with IP address and attempted payload
- **Rate limit violations** - Logged with client ID and endpoint
- **CSRF failures** - Logged with IP address and request path
- **Authentication failures** - Logged with IP address
- **Validation errors** - Logged with field and error details

Logs are written to:
- `logs/airzone.log` - All logs
- `logs/airzone_errors.log` - Errors only
- Console - Real-time monitoring

## Conclusion

Task 7 has been fully implemented with comprehensive security features and error handling mechanisms. All requirements (6.4, 6.5, 6.6, 6.7, 6.8, 8.7) are satisfied, and the implementation follows security best practices.
