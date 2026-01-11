"""Rate limiting utilities"""
import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Tuple

class RateLimiter:
    """Simple in-memory rate limiter (use Redis for production)"""
    
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.cleanup_interval = 3600  # Clean old entries every hour
        self.last_cleanup = time.time()
    
    def is_allowed(self, client_id: str, max_requests: int = 5, window_seconds: int = 60) -> bool:
        """
        Check if client has exceeded rate limit
        
        Args:
            client_id: Unique identifier (IP, user_id, email, etc.)
            max_requests: Max requests allowed in window
            window_seconds: Time window in seconds
            
        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        current_time = time.time()
        
        # Cleanup old entries periodically
        if current_time - self.last_cleanup > self.cleanup_interval:
            self._cleanup_old_entries(current_time)
            self.last_cleanup = current_time
        
        # Remove old requests outside the window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if current_time - req_time < window_seconds
        ]
        
        # Check if limit exceeded
        if len(self.requests[client_id]) >= max_requests:
            return False
        
        # Add current request
        self.requests[client_id].append(current_time)
        return True
    
    def get_remaining(self, client_id: str, max_requests: int = 5, window_seconds: int = 60) -> Tuple[int, int]:
        """
        Get remaining requests and reset time for client
        
        Returns:
            Tuple of (remaining_requests, seconds_until_reset)
        """
        current_time = time.time()
        
        # Remove old requests outside the window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if current_time - req_time < window_seconds
        ]
        
        remaining = max_requests - len(self.requests[client_id])
        reset_time = int(window_seconds) if remaining == 0 else 0
        
        return remaining, reset_time
    
    def _cleanup_old_entries(self, current_time: float):
        """Remove clients with no recent requests"""
        keys_to_delete = [
            key for key, times in self.requests.items()
            if not times or (current_time - max(times) > 3600)
        ]
        for key in keys_to_delete:
            del self.requests[key]


# Global rate limiter instance
rate_limiter = RateLimiter()
