from fastapi import FastAPI

app = FastAPI(title="Notification Service")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "notification"}

@app.get("/")
async def root():
    return {"message": "Notification Service"}