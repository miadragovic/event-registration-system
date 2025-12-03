from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        orm_mode = True


# ---------- AUTH / TOKEN ----------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    id: Optional[int] = None


# ---------- EVENT SCHEMAS ----------

class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventRead(EventBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ---------- REGISTRATION SCHEMAS ----------

class RegistrationBase(BaseModel):
    participant_name: str
    participant_email: str
    notes: Optional[str] = None


class RegistrationCreate(RegistrationBase):
    event_id: int


class RegistrationRead(RegistrationBase):
    id: int
    event_id: int
    event_name: Optional[str] = None
    event_date: Optional[datetime] = None
    event_location: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

