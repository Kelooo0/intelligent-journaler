from fastapi import FastAPI
from app.routers import auth, entries

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])

app.include_router(entries.router, prefix="/entries", tags=["entries"])


@app.get("/")
def main():
    return {"message": "App working properly"}
