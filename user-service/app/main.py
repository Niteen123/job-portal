from fastapi import FastAPI
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.logging import LoggingMiddleware

SERVICE_NAME = "juserservice"

app = FastAPI(title=SERVICE_NAME)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(LoggingMiddleware)

@app.get("/health")
def health():
    return {"status": "ok", "service": SERVICE_NAME}
