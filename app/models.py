from database import Base
from sqlalchemy import Table, Column, Integer, ForeignKey, Text, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

entry_tags = Table(
    'entry_tags',
    Base.metadata,
    Column('entry_id', Integer, ForeignKey('entries.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class JournalEntry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    summary = Column(String, nullable=True)
    mood = Column(String, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    tags = relationship('Tag', secondary=entry_tags, back_populates='entries')

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    entries = relationship('JournalEntry', secondary=entry_tags, back_populates='tags')

