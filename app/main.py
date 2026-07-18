from fastapi import FastAPI

from app.core.logging_config import setup_logging
from app.core.middleware import log_request_middleware
from app.routers import assistant, auth, entries

setup_logging()

app = FastAPI()

app.middleware("http")(log_request_middleware)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

app.include_router(entries.router, prefix="/entries", tags=["Entries"])

app.include_router(assistant.router, prefix="/assistant", tags=["Assistant"])


@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "ok", "project": "Intelligent Journaler API", "version": "1.0.0"}
