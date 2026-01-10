from fastapi import FastAPI

app = FastAPI(title="Resume Service")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "resume"}

@app.get("/")
async def root():
    return {"message": "Resume Service"}