from fastapi import APIRouter, HTTPException
from app.services.auth_client import AuthServiceClient

router = APIRouter(prefix="/api/auth", tags=["auth"])

auth_client = AuthServiceClient()

@router.post("/login")
async def login(payload: dict):
    try:
        return await auth_client.login(payload)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Auth service unavailable"
        )
