# app/core/config.py
import os

class Settings:
    PROJECT_NAME: str = "Job Portal API Gateway"

    AUTH_SERVICE_URL: str = os.getenv(
        "AUTH_SERVICE_URL", "http://auth-service:8000"
    )
    USER_SERVICE_URL: str = os.getenv(
        "USER_SERVICE_URL", "http://user-service:8000"
    )
    JOB_SERVICE_URL: str = os.getenv(
        "JOB_SERVICE_URL", "http://job-service:8000"
    )
    APPLICATION_SERVICE_URL: str = os.getenv(
        "APPLICATION_SERVICE_URL", "http://application-service:8000"
    )

settings = Settings()
