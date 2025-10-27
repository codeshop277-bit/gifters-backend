from fastapi import APIRouter, HTTPException, Depends, Header
from database import users_list, get_db
from sqlalchemy.orm import Session
from schemas import UserCreate, UserResponse, UserLogin, UserGuest, GuestResponse
from models import User, RefreshTokens
from utils.auth import hash_password, verify_password
from fastapi.security import OAuth2PasswordBearer
from utils.jwt_handlers import create_acces_token, verify_token, SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
import secrets

router = APIRouter(prefix="/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str= Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get('sub')
        if user_id is None:
            raise credential_exception
    
    except JWTError:
        raise credential_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return credential_exception
    
    return user
    # payload = verify_token(token)
    # if not payload:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="Invalid or expired token",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # return payload 

# @router.get("", response_model=list[UserResponse])
# def fetch_users_list(db: Session = Depends(get_db)):
#     return db.query(User).all()

@router.get("/search/{id}", response_model=UserResponse)
def search_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    result = next((user for user in users_list if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} does not exist")
    return user

@router.post("/post", response_model=UserResponse)
def post_user(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = User(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=401, detail=f"Email with id {user_data.email} already exists")
    
    print("Hashing password:", user_data.password)
    hash_pass = hash_password(user_data.password)
    print("Hashed:", hash_pass)
    new_user = User(name=user_data.name, password=user_data.password, hashed_password= hash_pass, email=user_data.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login/basic", response_model=UserResponse)
def login_user(user_data:UserLogin, db: Session=Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")
    if not verify_password(user_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalod credentials")
    
    return db_user

@router.post("/guest/login", response_model=GuestResponse)
def guest_login(user_data: UserGuest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        access_token = create_acces_token({"sub": db_user.email})
        refresh = secrets.token_hex(32)
        db.add(RefreshTokens(user_id= db_user.id, token=refresh))
        db.commit()
        return {"access_token": access_token, "user": UserResponse.from_orm(db_user)}
    else:
        new_user = User(name=user_data.name, email=user_data.email, auth_provider="google", mode="guest", provider_id = user_data.provider_id)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        reg_access_token = create_acces_token({"sub": new_user.email})
        reg_refresh = secrets.token_hex(32)
        db.add(RefreshTokens(user_id=new_user.id, token=reg_refresh))
        db.commit()
        return {"access_token": reg_access_token, "user": UserResponse.from_orm(new_user)}

@router.post("/login")
def login_user_token(user_data: UserLogin, db: Session=Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")
    if not verify_password(user_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_acces_token({"sub": db_user.email}) #sub is subject, what the token is about
    refresh = secrets.token_hex(32)
    print("token", db_user)
    db.add(RefreshTokens(user_id=db_user.id, token= refresh))
    db.commit()
    
    return {"access_token": access_token, "user": UserResponse.from_orm(db_user)} # returning a raw model instance like db_user will not be seialized to JSON so 
# it will always be {}. to counter this UserResponse.from_orm(db_user

@router.get("", response_model=list[UserResponse])
def fetch_users_list(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/logout")
def logout_user(refresh_token: str, db: Session = Depends(get_db)):
    deleted = db.query(RefreshTokens).filter(RefreshTokens.token == refresh_token).delete()
    if not deleted:
        raise HTTPException(status_code=401, detail="Token not found")
    
    db.commit()
    return {"msg": "User logged out successfully"}

@router.get("/refresh")
def refresh(refresh_token: str=Header(..., alias="X-Refresh-Token"), db: Session = Depends(get_db)):
    print(refresh_token)
    token = db.query(RefreshTokens).filter(RefreshTokens.token == refresh_token).first()
    print('token:::', token.user.email)
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    new_token= create_acces_token({"sub":  token.user.email})

    return {'access_token': new_token}