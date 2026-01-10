from fastapi import FastAPI

app = FastAPI(title="Employer Service")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "employer"}

@app.get("/")
async def root():
    return {"message": "Employer Service"}