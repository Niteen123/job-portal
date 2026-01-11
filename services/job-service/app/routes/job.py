from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.job import Job, Application
from app.schemas.job import (
    JobCreate, JobUpdate, JobResponse,
    ApplicationCreate, ApplicationUpdate, ApplicationResponse
)

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(job_data: JobCreate, user_id: int = Depends(lambda: 1), db: Session = Depends(get_db)):
    """
    Create a new job posting (employer only)
    
    - **title**: Job title
    - **description**: Job description
    - **company**: Company name
    - **location**: Job location
    - **salary_min**: Minimum salary (optional)
    - **salary_max**: Maximum salary (optional)
    - **job_type**: full_time, part_time, or contract
    - **requirements**: Job requirements
    """
    new_job = Job(
        title=job_data.title,
        description=job_data.description,
        company=job_data.company,
        location=job_data.location,
        salary_min=job_data.salary_min,
        salary_max=job_data.salary_max,
        job_type=job_data.job_type,
        requirements=job_data.requirements,
        posted_by_user_id=user_id
    )
    
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    return new_job


@router.get("", response_model=list[JobResponse])
def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    company: str = Query(None),
    location: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    List all active job postings with optional filters
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Number of records to return (max 100)
    - **company**: Filter by company name (optional)
    - **location**: Filter by location (optional)
    """
    query = db.query(Job).filter(Job.is_active == True)
    
    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))
    
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    
    jobs = query.offset(skip).limit(limit).all()
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Get a specific job by ID
    
    - **job_id**: Job ID
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    return job


@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    user_id: int = Depends(lambda: 1),
    db: Session = Depends(get_db)
):
    """
    Update a job posting (employer only)
    
    - **job_id**: Job ID
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    if job.posted_by_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this job"
        )
    
    # Update fields
    if job_data.title:
        job.title = job_data.title
    if job_data.description:
        job.description = job_data.description
    if job_data.location:
        job.location = job_data.location
    if job_data.salary_min is not None:
        job.salary_min = job_data.salary_min
    if job_data.salary_max is not None:
        job.salary_max = job_data.salary_max
    if job_data.job_type:
        job.job_type = job_data.job_type
    if job_data.requirements:
        job.requirements = job_data.requirements
    
    db.commit()
    db.refresh(job)
    
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    user_id: int = Depends(lambda: 1),
    db: Session = Depends(get_db)
):
    """
    Delete a job posting (employer only)
    
    - **job_id**: Job ID
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    if job.posted_by_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this job"
        )
    
    db.delete(job)
    db.commit()


# Application endpoints
@router.post("/{job_id}/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def apply_for_job(
    job_id: int,
    app_data: ApplicationCreate,
    user_id: int = Depends(lambda: 1),
    db: Session = Depends(get_db)
):
    """
    Apply for a job (job seeker only)
    
    - **job_id**: Job ID
    - **cover_letter**: Cover letter (optional)
    - **resume_url**: URL to resume (optional)
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Check if already applied
    existing_app = db.query(Application).filter(
        Application.job_id == job_id,
        Application.applicant_user_id == user_id
    ).first()
    
    if existing_app:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this job"
        )
    
    new_application = Application(
        job_id=job_id,
        applicant_user_id=user_id,
        cover_letter=app_data.cover_letter,
        resume_url=app_data.resume_url
    )
    
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    
    return new_application


@router.get("/{job_id}/applications", response_model=list[ApplicationResponse])
def get_job_applications(
    job_id: int,
    user_id: int = Depends(lambda: 1),
    db: Session = Depends(get_db)
):
    """
    Get all applications for a job (employer only)
    
    - **job_id**: Job ID
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    if job.posted_by_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view applications for this job"
        )
    
    applications = db.query(Application).filter(Application.job_id == job_id).all()
    return applications


@router.get("/user/{user_id}/applications", response_model=list[ApplicationResponse])
def get_user_applications(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all applications by a user (job seeker)
    
    - **user_id**: User ID
    """
    applications = db.query(Application).filter(
        Application.applicant_user_id == user_id
    ).all()
    
    return applications


@router.put("/applications/{app_id}", response_model=ApplicationResponse)
def update_application_status(
    app_id: int,
    app_data: ApplicationUpdate,
    user_id: int = Depends(lambda: 1),
    db: Session = Depends(get_db)
):
    """
    Update application status (employer only)
    
    - **app_id**: Application ID
    - **status**: New status (applied, reviewed, shortlisted, rejected, hired)
    """
    application = db.query(Application).filter(Application.id == app_id).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    job = db.query(Job).filter(Job.id == application.job_id).first()
    
    if job.posted_by_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this application"
        )
    
    application.status = app_data.status
    db.commit()
    db.refresh(application)
    
    return application
