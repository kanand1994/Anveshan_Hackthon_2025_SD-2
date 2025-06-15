from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from backend.database import get_db
from backend import schemas, crud
from .auth import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/timeline", response_model=schemas.Timeline)
def get_timeline(db: Session = Depends(get_db),
                current_user: schemas.User = Depends(get_current_user)):
    try:
        # Calculate weeks lived
        birthdate = current_user.birthdate
        today = datetime.utcnow().date()
        weeks_lived = (today - birthdate).days // 7
        logger.info(f"Getting timeline for user: {current_user.email}")
        logger.info(f"Birthdate: {birthdate}")
        logger.info(f"Weeks lived: {weeks_lived}")
        
        # Get events
        events = crud.get_events_by_user(db, user_id=current_user.id)
        logger.info(f"Found {len(events)} events")
        
        # Structure timeline
        timeline = []
        for week_num in range(weeks_lived + 1):
            start_date = birthdate + timedelta(weeks=week_num)
            end_date = start_date + timedelta(days=6)
            
            week_events = [
                schemas.Event(
                    id=event.id,
                    user_id=event.user_id,
                    date=event.date,
                    title=event.title,
                    description=event.description,
                    category=event.category
                )
                for event in events
                if start_date <= event.date <= end_date
            ]
            
            timeline.append(schemas.Week(
                week_number=week_num,
                start_date=start_date,
                end_date=end_date,
                events=week_events
            ))
        
        logger.info(f"Created timeline with {len(timeline)} weeks")
        return {"weeks": timeline}
    
    except Exception as e:
        logger.exception(f"Error in timeline generation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")