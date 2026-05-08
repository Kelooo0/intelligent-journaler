from app.database import Base
from sqlalchemy import Table, Column, Integer, ForeignKey, Text, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    entries = relationship('EntryModel', back_populates='owner')

entry_tags = Table(
    'entry_tags',
    Base.metadata,
    Column('entry_id', Integer, ForeignKey('entries.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class EntryModel(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    summary = Column(String, nullable=True)
    mood = Column(String, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship('UserModel', back_populates='entries')
    tags = relationship('TagModel', secondary=entry_tags, back_populates='entries')

class TagModel(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    entries = relationship('EntryModel', secondary=entry_tags, back_populates='tags')

