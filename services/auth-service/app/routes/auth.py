from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.user import User, TokenBlacklist
from app.schemas import (
    UserRegister, UserLogin, UserResponse, LoginResponse,
    RefreshTokenRequest, RefreshTokenResponse,
    PasswordResetRequest, PasswordResetConfirm, PasswordResetResponse
)
from app.utils.password import hash_password, verify_password
from app.utils.jwt import (
    create_access_token, create_refresh_token, create_password_reset_token, decode_token
)
from app.utils.rate_limit import rate_limiter
from app.dependencies import get_current_user
import secrets

router = APIRouter(prefix="/auth", tags=["auth"])

# Rate limiting configuration
REGISTER_MAX_REQUESTS = 5
REGISTER_WINDOW = 60 * 60  # 1 hour
LOGIN_MAX_REQUESTS = 10
LOGIN_WINDOW = 60 * 5  # 5 minutes


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, request: Request, db: Session = Depends(get_db)):
    """
    Register a new user with rate limiting
    
    - **email**: User email (must be unique)
    - **password**: Plain password (will be hashed)
    - **full_name**: User's full name
    - **role**: job_seeker or employer (default: job_seeker)
    """
    # Rate limiting by IP
    client_ip = request.client.host if request.client else "unknown"
    if not rate_limiter.is_allowed(f"register:{client_ip}", REGISTER_MAX_REQUESTS, REGISTER_WINDOW):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many registration attempts. Try again later."
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    
    # Create user
    new_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=LoginResponse)
def login(credentials: UserLogin, request: Request, db: Session = Depends(get_db)):
    """
    Login user and return JWT tokens
    
    - **email**: User email
    - **password**: Plain password
    """
    # Rate limiting by IP
    client_ip = request.client.host if request.client else "unknown"
    if not rate_limiter.is_allowed(f"login:{client_ip}", LOGIN_MAX_REQUESTS, LOGIN_WINDOW):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Try again later."
        )
    
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    # Store refresh token in DB
    user.refresh_token = refresh_token
    db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh_access_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token
    
    - **refresh_token**: Valid refresh token from login response
    """
    payload = decode_token(request.refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user or user.refresh_token != request.refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Create new access token
    new_access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Logout user by invalidating tokens
    """
    # Clear refresh token
    current_user.refresh_token = None
    db.commit()
    
    return {"message": "Successfully logged out"}


@router.post("/reset-password-request", response_model=PasswordResetResponse)
def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    Request password reset - generates reset token
    
    - **email**: User's email address
    """
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        # Don't reveal if email exists (security best practice)
        return {"message": "If email exists, password reset token has been sent"}
    
    # Generate password reset token
    reset_token = create_password_reset_token(user.id)
    
    # Store token with expiration (1 hour)
    user.password_reset_token = reset_token
    user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    
    # In production, send email with reset link
    # For now, just return success message
    return {"message": "Password reset token sent to email"}


@router.post("/reset-password-confirm", response_model=PasswordResetResponse)
def confirm_password_reset(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    """
    Confirm password reset with token
    
    - **token**: Password reset token from email
    - **new_password**: New password to set
    """
    payload = decode_token(request.token)
    
    if not payload or payload.get("type") != "password_reset":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user or user.password_reset_token != request.token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )
    
    # Check if token expired
    if user.password_reset_expires and user.password_reset_expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )
    
    # Update password
    user.password_hash = hash_password(request.new_password)
    user.password_reset_token = None
    user.password_reset_expires = None
    db.commit()
    
    return {"message": "Password successfully reset"}
