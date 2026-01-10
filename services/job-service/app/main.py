from fastapi import FastAPI

app = FastAPI(title="Job Service")

@app.get("/health")
def health():
    return {"status": "ok", "service": "job"}

@app.get("/jobs")
def get_jobs():
    return {
        "jobs": [
            {"id": 1, "title": "Backend Engineer"},
            {"id": 2, "title": "Python Developer"}
        ]
    }
