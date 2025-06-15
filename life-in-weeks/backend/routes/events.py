from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import schemas, crud
from .auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from backend.config import SECRET_KEY, ALGORITHM
import logging
from datetime import date, datetime, timedelta
from backend.models import User 

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
logger = logging.getLogger(__name__)

# Then update the get_current_user function
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print(f"Received token: {token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        print(f"Decoded email: {email}")
        if email is None:
            print("Email not found in token")
            raise credentials_exception
    except JWTError as e:
        print(f"JWT Error: {str(e)}")
        raise credentials_exception
    
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        print(f"User not found for email: {email}")
        raise credentials_exception
    return user
@router.get("/", response_model=list[schemas.Event])  # Changed endpoint to root path
def read_events(skip: int = 0, limit: int = 100,
               db: Session = Depends(get_db),
               current_user: schemas.User = Depends(get_current_user)):
    return crud.get_events(db, user_id=current_user.id, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, 
                db: Session = Depends(get_db),
                current_user: schemas.User = Depends(get_current_user)):
    print(f"Creating event for user: {current_user.email}")
    return crud.create_event(db=db, event=event, user_id=current_user.id)

@router.get("/{event_id}", response_model=schemas.Event)
def read_event(event_id: int,
              db: Session = Depends(get_db),
              current_user: schemas.User = Depends(get_current_user)):
    try:
        logger.info(f"Fetching event {event_id} for user {current_user.email}")
        db_event = crud.get_event(db, event_id=event_id)
        if not db_event or db_event.user_id != current_user.id:
            logger.warning(f"Event not found or unauthorized: {event_id}")
            raise HTTPException(status_code=404, detail="Event not found")
        return db_event
    except Exception as e:
        logger.exception(f"Error fetching event {event_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{event_id}", response_model=schemas.Event)
def update_event(event_id: int, event: schemas.EventUpdate,
                db: Session = Depends(get_db),
                current_user: schemas.User = Depends(get_current_user)):
    db_event = crud.get_event(db, event_id=event_id)
    if not db_event or db_event.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Event not found")
    return crud.update_event(db=db, event_id=event_id, event=event)

@router.delete("/{event_id}")
def delete_event(event_id: int,
                db: Session = Depends(get_db),
                current_user: schemas.User = Depends(get_current_user)):
    db_event = crud.get_event(db, event_id=event_id)
    if not db_event or db_event.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Event not found")
    return crud.delete_event(db=db, event_id=event_id)
    
@router.get("/summary", response_model=schemas.EventSummary)
def get_events_summary(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    return crud.get_event_summary(db, user_id=current_user.id)

@router.post("/{event_id}/restore", response_model=schemas.Event)
def restore_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_event = crud.get_event(db, event_id=event_id)
    if not db_event or db_event.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Event not found")
    return crud.restore_event(db, event_id=event_id)
    
@router.get("/summary")
async def get_events_summary(
    request: Request,  # Add this parameter
    start_date: date = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: date = Query(..., description="End date in YYYY-MM-DD format"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Log detailed request information
    logger.info(f"Summary request received from {current_user.email}")
    logger.info(f"Query params: {request.query_params}")
    logger.info(f"Start date: {start_date}, End date: {end_date}")
    
    today = datetime.now().date()
    start_date = start_date or date(today.year, 1, 1)
    end_date = end_date or date(today.year, 12, 31)
    
    logger.info(f"Using date range: {start_date} to {end_date}")
    
    """
    Get summary of events within a date range
    """
    # Get events for the current user in the date range
    events = crud.get_events_by_date_range(
        db, 
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )
    
    # Create a simple summary
    summary = {
        "total_events": len(events),
        "categories": {},
        "earliest_event": min([e.date for e in events]) if events else None,
        "latest_event": max([e.date for e in events]) if events else None
    }
    
    # Count events by category
    for event in events:
        summary["categories"][event.category] = summary["categories"].get(event.category, 0) + 1
    
    return summary