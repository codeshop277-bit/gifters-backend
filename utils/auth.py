from passlib.context import CryptContext
#Passlib is a Python library for handling password hashing securely.
#CryptContext is a central object in Passlib that manages different hashing algorithms

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

#schemes tells passlib to use brcypt algorithm for hashing
#deprecetaed is set so when upgraded to diff scheme, passlib will mark older ones as deprecated and rehash password when user logsin

def hash_password(password: str) -> str: #arrow function type hint for return value
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password) -> str:
    return pwd_context.verify(plain_password, hashed_password)