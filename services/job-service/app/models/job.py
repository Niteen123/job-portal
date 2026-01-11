from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    company = Column(String, nullable=False, index=True)
    location = Column(String, nullable=False)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    job_type = Column(String, default="full_time")  # full_time, part_time, contract
    requirements = Column(Text, nullable=False)
    posted_by_user_id = Column(Integer, nullable=False)  # Employer ID
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Job(id={self.id}, title={self.title}, company={self.company})>"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    applicant_user_id = Column(Integer, nullable=False)  # Job seeker ID
    status = Column(String, default="applied")  # applied, reviewed, shortlisted, rejected, hired
    cover_letter = Column(Text, nullable=True)
    resume_url = Column(String, nullable=True)
    applied_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Application(id={self.id}, job_id={self.job_id}, applicant_id={self.applicant_user_id})>"
