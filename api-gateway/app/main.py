# app/main.py
from fastapi import FastAPI

from app.core.config import settings
from app.routes import auth, user, job

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/health")
def health():
    return {"status": "ok", "service": "api-gateway"}

# Register routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(job.router)
