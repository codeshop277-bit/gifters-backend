from passlib.context import CryptContext
#Passlib is a Python library for handling password hashing securely.
#CryptContext is a central object in Passlib that manages different hashing algorithms

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database import get_db
from models import User


pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "protected"  
ALGORITHM = "HS256"  

#schemes tells passlib to use brcypt algorithm for hashing
#deprecetaed is set so when upgraded to diff scheme, passlib will mark older ones as deprecated and rehash password when user logsin

def hash_password(password: str) -> str: #arrow function type hint for return value
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password) -> str:
    return pwd_context.verify(plain_password, hashed_password)



def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("SECRET_KEY:", SECRET_KEY)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload", payload)
        email: str = payload.get("sub")
        print(email)
        if email is None:
            raise credentials_exception
    except JWTError as e:
        print("JWT error:", str(e))
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
