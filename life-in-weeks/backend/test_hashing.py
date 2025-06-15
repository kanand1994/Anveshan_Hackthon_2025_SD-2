import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from security import hash_password, verify_password

def test_password_hashing():
    password = "password"
    print(f"Testing password: {password}")
    
    hashed = hash_password(password)
    print(f"Hashed password: {hashed}")
    
    # Verify with correct password
    print("\nTesting correct password:")
    result = verify_password(password, hashed)
    print(f"Verification result: {result}")
    
    # Verify with incorrect password
    print("\nTesting incorrect password:")
    result = verify_password("wrongpassword", hashed)
    print(f"Verification result: {result}")

if __name__ == "__main__":
    test_password_hashing()