from fastapi import APIRouter, HTTPException, Depends
from database import users_list, get_db
from sqlalchemy.orm import Session
from schemas import UserCreate, UserResponse, UserLogin
from models import User
from utils.auth import hash_password, verify_password

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=list[UserResponse])
def fetch_users_list(db: Session = Depends(get_db)):
    return db.query(User).all()

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
    new_user = User(name=user_data.name, password=hash_pass, email=user_data.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=UserResponse)
def login_user(user_data:UserLogin, db: Session=Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")
    if not verify_password(user_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalod credentials")
    
    return db_user
    