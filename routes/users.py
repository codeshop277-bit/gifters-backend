from fastapi import APIRouter, HTTPException, Depends
from database import users_list, get_db
from sqlalchemy.orm import Session
from schemas import UserCreate, UserResponse
from models import User

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