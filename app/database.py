from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    settings.DATABASE_URL, connect_args={"options": "-c client_encoding=utf-8"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
