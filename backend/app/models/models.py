from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
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

    __table_args__ = (Index("ix_entries_user_id_created_at", "user_id", "created_at"),)

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    summary = Column(String, nullable=True)
    mood = Column(String, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    embedding = Column(Vector(1536), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("UserModel", back_populates="entries", lazy="joined")
    tags = relationship(
        "TagModel", secondary=entry_tags, back_populates="entries", lazy="selectin"
    )


class TagModel(Base):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_user_id_name"),)

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    entries = relationship(
        "EntryModel", secondary=entry_tags, back_populates="tags", lazy="selectin"
    )
