from fastapi import FastAPI
from app.routers import auth, entries

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])

app.include_router(entries.router, prefix="/entries", tags=["entries"])


@app.get("/", tags=["Health Check"])
def health_check():
    return {
        "status": "ok",
        "project": "Intelligent Journaler API",
        "version": "1.0.0"
        }
