"""Logging middleware for HTTP requests and responses."""
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log HTTP requests and responses."""

    async def dispatch(self, request: Request, call_next):
        """Log request and response details."""
        start_time = time.time()
        request_id = getattr(request.state, "request_id", "unknown")
        
        logger.info(
            f"Request: {request.method} {request.url.path}",
            extra={"request_id": request_id}
        )
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} - Duration: {process_time:.3f}s",
            extra={"request_id": request_id}
        )
        
        return response
