from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from backend.database import get_db
from backend import crud, schemas, models
from backend.crud import pwd_context
from backend.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES  # Updated import
from backend.security import verify_password
import hashlib
router = APIRouter()

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/signup", response_model=schemas.User)
async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(f"Signing up user: {user.email}")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    created_user = crud.create_user(db=db, user=user)
    print(f"Created user with hash: {created_user.hashed_password}")
    return created_user

@router.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"🔑 Login attempt for: {form_data.username}")
    
    db_user = crud.get_user_by_email(db, email=form_data.username)
    
    if not db_user:
        print("❌ User not found in database")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"ℹ️ User found: {db_user.email}")
    print(f"🔐 Stored hash: {db_user.hashed_password}")
    
    # Verify password
    try:
        # Split the stored hash
        parts = db_user.hashed_password.split("$")
        if len(parts) != 3:
            print("⚠️ Invalid hash format")
            raise ValueError("Invalid hash format")
            
        algorithm, salt, stored_hash = parts
        print(f"🔧 Using algorithm: {algorithm}, salt: {salt}")
        
        # Compute the hash for the provided password
        computed_hash = hashlib.sha256((form_data.password + salt).encode()).hexdigest()
        print(f"🔧 Computed hash: {computed_hash}")
        
        # Compare hashes
        if computed_hash == stored_hash:
            print("✅ Password verification successful")
        else:
            print("❌ Password verification failed")
            print(f"Provided: {form_data.password}")
            print(f"Expected: {stored_hash}")
            print(f"Actual: {computed_hash}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
    except Exception as e:
        print(f"⚠️ Verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Token generation
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + access_token_expires
    
    payload = {
        "sub": db_user.email,
        "exp": expire
    }
    
    access_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    print(f"🔑 Generated token: {access_token}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/diagnostics")
def diagnostics(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    result = []
    
    for user in users:
        result.append({
            "id": user.id,
            "email": user.email,
            "birthdate": str(user.birthdate),
            "hashed_password": user.hashed_password,
            "password_length": len(user.hashed_password) if user.hashed_password else 0
        })
    
    return result
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user
    
__all__ = ["router", "SECRET_KEY", "ALGORITHM"]
@router.get("/verify-token")
async def verify_token(current_user: schemas.User = Depends(get_current_user)):
    return {"email": current_user.email, "id": current_user.id}