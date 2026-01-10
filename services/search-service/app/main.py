from fastapi import FastAPI

app = FastAPI(title="Search Service")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "search"}

@app.get("/")
async def root():
    return {"message": "Search Service"}