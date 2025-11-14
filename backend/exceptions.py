"""Custom exception classes for the Airzone application"""


class AirzoneException(Exception):
    """Base exception class for Airzone application"""
    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationError(AirzoneException):
    """Exception raised for validation errors"""
    def __init__(self, message: str):
        super().__init__(message, code=400)


class AuthenticationError(AirzoneException):
    """Exception raised for authentication failures"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code=401)


class AuthorizationError(AirzoneException):
    """Exception raised for authorization failures"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, code=403)


class ResourceNotFoundError(AirzoneException):
    """Exception raised when a resource is not found"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, code=404)


class ResourceConflictError(AirzoneException):
    """Exception raised for resource conflicts"""
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message, code=409)


class ExternalServiceError(AirzoneException):
    """Exception raised for external service errors"""
    def __init__(self, message: str = "External service error"):
        super().__init__(message, code=502)


class DatabaseError(AirzoneException):
    """Exception raised for database errors"""
    def __init__(self, message: str = "Database error"):
        super().__init__(message, code=500)
