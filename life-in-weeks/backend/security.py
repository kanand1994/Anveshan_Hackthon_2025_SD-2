import hashlib
import os
import binascii

def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt"""
    salt = binascii.hexlify(os.urandom(16)).decode()
    pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"sha256${salt}${pwd_hash}"

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password"""
    if not hashed_password or "$" not in hashed_password:
        return False
        
    _, salt, stored_hash = hashed_password.split("$", 2)
    pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return pwd_hash == stored_hash