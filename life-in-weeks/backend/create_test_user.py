import os
import sys
from datetime import date

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User
from security import hash_password  # Or pwd_context if using Passlib

# Create database tables
Base.metadata.create_all(bind=engine)

def create_test_user():
    db = SessionLocal()
    
    # Delete existing test user if exists
    existing_user = db.query(User).filter(User.email == "test@example.com").first()
    if existing_user:
        db.delete(existing_user)
        db.commit()
    
    # Create new test user
    test_user = User(
        email="test@example.com",
        hashed_password=hash_password("password"),  # Use your chosen method
        birthdate=date(1990, 1, 1)
    )
    
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    print(f"Created test user with ID: {test_user.id}")
    db.close()

if __name__ == "__main__":
    create_test_user()