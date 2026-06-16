from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    entries = relationship("EntryModel", back_populates="owner", lazy="selectin")


entry_tags = Table(
    "entry_tags",
    Base.metadata,
    Column("entry_id", Integer, ForeignKey("entries.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class EntryModel(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    summary = Column(String, nullable=True)
    mood = Column(String, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    embedding = Column(Vector(768), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("UserModel", back_populates="entries", lazy="joined")
    tags = relationship(
        "TagModel", secondary=entry_tags, back_populates="entries", lazy="selectin"
    )


class TagModel(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    entries = relationship(
        "EntryModel", secondary=entry_tags, back_populates="tags", lazy="selectin"
    )
