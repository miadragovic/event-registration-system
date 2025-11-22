from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    date = Column(DateTime)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    participant_name = Column(String, nullable=False)
    participant_email = Column(String, nullable=False)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
