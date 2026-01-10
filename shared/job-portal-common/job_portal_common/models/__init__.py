"""Shared common models for all microservices."""
from typing import Any, Optional
from pydantic import BaseModel, Field
from enum import Enum


class UserRole(str, Enum):
    """User roles in the system."""
    JOB_SEEKER = "job_seeker"
    EMPLOYER = "employer"
    ADMIN = "admin"


class UserResponse(BaseModel):
    """Standard user response model."""
    id: int
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    is_verified: bool
    
    class Config:
        from_attributes = True


class JobResponse(BaseModel):
    """Standard job response model."""
    id: int
    title: str
    description: str
    company_id: int
    location: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    job_type: str  # full-time, part-time, contract, remote
    status: str = "active"
    created_at: str
    
    class Config:
        from_attributes = True


class ApplicationResponse(BaseModel):
    """Standard application response model."""
    id: int
    job_id: int
    user_id: int
    status: str  # pending, reviewed, rejected, accepted
    applied_date: str
    
    class Config:
        from_attributes = True


class StandardResponse(BaseModel):
    """Standard API response wrapper."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None
    status_code: int = 200


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)
    skip: int = Field(default=0)

    def get_offset(self) -> int:
        """Calculate offset for database query."""
        return (self.page - 1) * self.page_size
