"""Shared exceptions for all microservices."""


class AppException(Exception):
    """Base exception for the application."""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(AppException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401)


class AuthorizationError(AppException):
    """Raised when user doesn't have permission."""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, 403)


class NotFoundError(AppException):
    """Raised when resource is not found."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class ConflictError(AppException):
    """Raised when there's a conflict (e.g., duplicate email)."""
    
    def __init__(self, message: str = "Conflict"):
        super().__init__(message, 409)


class ValidationError(AppException):
    """Raised when validation fails."""
    
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, 400)


class ServiceUnavailableError(AppException):
    """Raised when a service is unavailable."""
    
    def __init__(self, service_name: str):
        super().__init__(f"{service_name} is currently unavailable", 503)


class InvalidTokenError(AuthenticationError):
    """Raised when token is invalid or expired."""
    
    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message)
