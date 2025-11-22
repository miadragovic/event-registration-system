from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventRead(EventBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class RegistrationBase(BaseModel):
    participant_name: str
    participant_email: str
    notes: Optional[str] = None

class RegistrationCreate(RegistrationBase):
    event_id: int

class RegistrationRead(RegistrationBase):
    id: int
    event_id: int
    created_at: datetime

    class Config:
        orm_mode = True
