from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from datetime import date, datetime
from typing import List, Optional

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    birthdate: date

class User(UserBase):
    id: int
    birthdate: date
    model_config = ConfigDict(from_attributes=True)

class EventBase(BaseModel):
    date: date
    title: str
    description: Optional[str] = None
    category: str

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class Event(EventBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class Week(BaseModel):
    week_number: int
    start_date: date
    end_date: date
    events: List[Event] = []

class Timeline(BaseModel):
    weeks: List[Week]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    
class EventWithDeleted(EventBase):
    id: int
    user_id: int
    deleted_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class EventSummary(BaseModel):
    past: List[EventWithDeleted] = []
    present: List[EventWithDeleted] = []
    future: List[EventWithDeleted] = []
    deleted: List[EventWithDeleted] = []