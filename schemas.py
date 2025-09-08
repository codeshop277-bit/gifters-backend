# schemas.py
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True   # 👈 allows returning SQLAlchemy objects

class GiftTemplate(BaseModel):
    name: str
    brand: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None

class GiftResponse(GiftTemplate):
    id: int
    user_id: int

    class Config:
        orm_mode = True

