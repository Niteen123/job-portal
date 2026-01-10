from fastapi import FastAPI

app = FastAPI(title="Auth Service")

@app.get("/health")
def health():
    return {"status": "ok", "service": "auth"}

@app.post("/login")
def login(payload: dict):
    return {
        "access_token": "dummy-jwt-token",
        "token_type": "bearer"
    }
