from fastapi import FastAPI
from app.core.database import engine, Base
from app.routes import auth, user
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.logging import LoggingMiddleware

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service",
    description="Authentication and user management service",
    version="0.1.0"
)

# Add middleware
app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(auth.router)
app.include_router(user.router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "auth-service"}
