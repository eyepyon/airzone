"""Custom exception classes for the Airzone application"""

from typing import Optional, Dict, Any


class AirzoneException(Exception):
    """Base exception class for Airzone application"""
    def __init__(self, message: str, code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for JSON response"""
        response = {
            'status': 'error',
            'error': self.message,
            'code': self.code
        }
        if self.details:
            response['details'] = self.details
        return response


class ValidationError(AirzoneException):
    """Exception raised for validation errors"""
    def __init__(self, message: str, field: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        if field and not details:
            details = {'field': field}
        elif field and details:
            details['field'] = field
        super().__init__(message, code=400, details=details)


class AuthenticationError(AirzoneException):
    """Exception raised for authentication failures"""
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code=401, details=details)


class AuthorizationError(AirzoneException):
    """Exception raised for authorization failures"""
    def __init__(self, message: str = "Insufficient permissions", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code=403, details=details)


class ResourceNotFoundError(AirzoneException):
    """Exception raised when a resource is not found"""
    def __init__(self, resource_type: str = "Resource", resource_id: Optional[str] = None):
        message = f"{resource_type} not found"
        details = {}
        if resource_id:
            message = f"{resource_type} with id '{resource_id}' not found"
            details['resource_id'] = resource_id
        details['resource_type'] = resource_type
        super().__init__(message, code=404, details=details)


class ResourceConflictError(AirzoneException):
    """Exception raised for resource conflicts"""
    def __init__(self, message: str = "Resource conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code=409, details=details)


class RateLimitExceededError(AirzoneException):
    """Exception raised when rate limit is exceeded"""
    def __init__(self, message: str = "Rate limit exceeded", retry_after: Optional[int] = None):
        details = {}
        if retry_after:
            details['retry_after'] = retry_after
        super().__init__(message, code=429, details=details)


class ExternalServiceError(AirzoneException):
    """Exception raised for external service errors"""
    def __init__(self, service_name: str, message: str = "External service error", details: Optional[Dict[str, Any]] = None):
        if not details:
            details = {}
        details['service'] = service_name
        super().__init__(message, code=502, details=details)


class DatabaseError(AirzoneException):
    """Exception raised for database errors"""
    def __init__(self, message: str = "Database error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code=500, details=details)


class InsufficientStockError(ResourceConflictError):
    """Exception raised when product stock is insufficient"""
    def __init__(self, product_id: str, requested: int, available: int):
        message = f"Insufficient stock for product {product_id}"
        details = {
            'product_id': product_id,
            'requested': requested,
            'available': available
        }
        super().__init__(message, details=details)


class NFTRequirementError(AuthorizationError):
    """Exception raised when NFT requirement is not met"""
    def __init__(self, required_nft_id: str, message: str = "Required NFT not found"):
        details = {
            'required_nft_id': required_nft_id,
            'reason': 'nft_requirement_not_met'
        }
        super().__init__(message, details=details)


class PaymentError(AirzoneException):
    """Exception raised for payment processing errors"""
    def __init__(self, message: str = "Payment processing failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code=400, details=details)


class BlockchainError(ExternalServiceError):
    """Exception raised for blockchain-related errors"""
    def __init__(self, message: str = "Blockchain operation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__("Sui Blockchain", message, details)
