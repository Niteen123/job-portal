from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class JobCreate(BaseModel):
    """Schema for creating a job posting"""
    title: str
    description: str
    company: str
    location: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    job_type: Optional[str] = "full_time"
    requirements: str


class JobUpdate(BaseModel):
    """Schema for updating a job posting"""
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    job_type: Optional[str] = None
    requirements: Optional[str] = None


class JobResponse(BaseModel):
    """Schema for job response"""
    id: int
    title: str
    description: str
    company: str
    location: str
    salary_min: Optional[float]
    salary_max: Optional[float]
    job_type: str
    requirements: str
    posted_by_user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    """Schema for creating an application"""
    job_id: int
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None


class ApplicationUpdate(BaseModel):
    """Schema for updating application status"""
    status: str  # applied, reviewed, shortlisted, rejected, hired


class ApplicationResponse(BaseModel):
    """Schema for application response"""
    id: int
    job_id: int
    applicant_user_id: int
    status: str
    cover_letter: Optional[str]
    resume_url: Optional[str]
    applied_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
