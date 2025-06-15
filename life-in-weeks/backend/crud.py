from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from backend.security import hash_password, verify_password
from datetime import datetime, date


pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        email=user.email, 
        hashed_password=hashed_password,
        birthdate=user.birthdate
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_events(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Event).filter(models.Event.user_id == user_id).offset(skip).limit(limit).all()

def get_events_by_user(db: Session, user_id: int):
    return db.query(models.Event).filter(models.Event.user_id == user_id).all()

def create_event(db: Session, event: schemas.EventCreate, user_id: int):
    db_event = models.Event(**event.dict(), user_id=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def update_event(db: Session, event_id: int, event: schemas.EventUpdate):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        for key, value in event.dict().items():
            setattr(db_event, key, value)
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event
    
def get_events_with_deleted(db: Session, user_id: int):
    return db.query(models.Event).filter(models.Event.user_id == user_id).all()

def soft_delete_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db_event.deleted_at = datetime.utcnow()
        db.commit()
        db.refresh(db_event)
    return db_event

def restore_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db_event.deleted_at = None
        db.commit()
        db.refresh(db_event)
    return db_event

def get_event_summary(db: Session, user_id: int):
    today = date.today()
    events = get_events_with_deleted(db, user_id)
    
    summary = {
        "past": [],
        "present": [],
        "future": [],
        "deleted": []
    }
    
    for event in events:
        if event.deleted_at:
            summary["deleted"].append(event)
        elif event.date < today:
            summary["past"].append(event)
        elif event.date == today:
            summary["present"].append(event)
        else:
            summary["future"].append(event)
            
    return summary