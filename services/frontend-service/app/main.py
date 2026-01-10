from fastapi import FastAPI

app = FastAPI(title="Frontend Service")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "frontend"}

@app.get("/")
async def root():
    return {"message": "Frontend Service"}
