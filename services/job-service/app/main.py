from fastapi import FastAPI
from app.core.database import engine, Base
from app.routes import job
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Job Service",
    description="Job posting and application management",
    version="1.0.0"
)

# Create all database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(job.router)


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "job-service"}


@app.on_event("startup")
async def startup_event():
    logger.info("Job Service starting up")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Job Service shutting down")
