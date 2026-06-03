from fastapi import FastAPI

from app.routers import auth, entries

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

app.include_router(entries.router, prefix="/entries", tags=["Entries"])


@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "ok", "project": "Intelligent Journaler API", "version": "1.0.0"}
