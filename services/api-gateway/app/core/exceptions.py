"""Global exception handlers for API Gateway."""
import logging
from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


class ServiceUnavailableError(Exception):
    """Exception for when a downstream service is unavailable."""
    pass


async def global_exception_handler(request: Request, exc: Exception):
    """Handle global exceptions and return consistent error responses."""
    request_id = getattr(request.state, "request_id", "unknown")
    
    logger.error(
        f"Exception: {str(exc)}",
        extra={"request_id": request_id},
        exc_info=True
    )
    
    # Handle specific exception types
    if isinstance(exc, ServiceUnavailableError):
        return JSONResponse(
            status_code=503,
            content={
                "error": "Service Unavailable",
                "detail": str(exc),
                "request_id": request_id
            }
        )
    
    # Default error response
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred",
            "request_id": request_id
        }
    )
