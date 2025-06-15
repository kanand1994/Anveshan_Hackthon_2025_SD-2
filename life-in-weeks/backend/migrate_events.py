from backend.database import SessionLocal, engine
from backend.models import Event, Base
from datetime import datetime

def migrate_events():
    db = SessionLocal()
    
    # Add deleted_at column if not exists
    print("Migrating events table...")
    
    # For SQLite, we need to create a new table
    # This is a simplified migration for SQLite
    Base.metadata.drop_all(bind=engine, tables=[Event.__table__])
    Base.metadata.create_all(bind=engine, tables=[Event.__table__])
    
    print("Migration complete. Please note: All existing events were reset.")
    
    db.close()

if __name__ == "__main__":
    migrate_events()