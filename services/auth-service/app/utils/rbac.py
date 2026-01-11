"""Role-Based Access Control utilities"""
from functools import wraps
from fastapi import HTTPException, status
from typing import List

def require_role(*required_roles: str):
    """
    Decorator to enforce role-based access control
    
    Usage:
        @require_role("employer", "admin")
        async def my_route(current_user: User = Depends(get_current_user)):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from kwargs (passed by FastAPI dependency injection)
            current_user = kwargs.get('current_user')
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
            
            if current_user.role not in required_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"This endpoint requires one of these roles: {', '.join(required_roles)}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def check_role(user_role: str, required_roles: List[str]) -> bool:
    """Check if user role is in required roles list"""
    return user_role in required_roles
