from fastapi import APIRouter, HTTPException
from app.services.user_client import UserServiceClient

router = APIRouter(prefix="/api/users", tags=["users"])

user_client = UserServiceClient()

@router.get("/{user_id}")
async def get_user(user_id: int):
    try:
        return await user_client.get_user(user_id)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="User service unavailable"
        )
