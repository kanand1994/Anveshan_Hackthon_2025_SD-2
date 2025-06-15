from sqlalchemy import Column, Integer, String, Date, ForeignKey
from backend.database import Base
from sqlalchemy import DateTime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    birthdate = Column(Date)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    title = Column(String, index=True)
    description = Column(String)
    category = Column(String)
    deleted_at = Column(DateTime, nullable=True)