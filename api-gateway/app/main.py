# app/main.py
from fastapi import FastAPI

from app.core.config import settings
from app.routes import auth, user, job
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.logging import LoggingMiddleware
from app.core.exceptions import global_exception_handler

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/health")
def health():
    return {"status": "ok", "service": "api-gateway"}

# Register routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(job.router)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_exception_handler(Exception, global_exception_handler)


