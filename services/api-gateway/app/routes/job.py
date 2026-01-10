from fastapi import APIRouter, HTTPException
from app.services.job_client import JobServiceClient

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

job_client = JobServiceClient()

@router.get("")
async def list_jobs():
    try:
        return await job_client.get_jobs()
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Job service unavailable"
        )
