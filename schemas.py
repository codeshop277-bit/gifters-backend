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
    
class UserGuest(BaseModel):
    email: str
    name: str
    provider_id: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True   # 👈 allows returning SQLAlchemy objects

class GuestResponse(BaseModel):
    user: UserResponse
    access_token: str

class GiftTemplate(BaseModel):
    name: str
    brand: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    link:  Optional[str] = None
    note: Optional[str] = None
    price: int

class GiftResponse(GiftTemplate):
    id: int
    user_id: int
    link: Optional[str]
    price: Optional[int]
    claimed: Optional[bool]
    name: Optional[str]

    class Config:
        orm_mode = True

class GiftOut(BaseModel):
    id: int
    claimed: bool
    claimed_by: Optional[str] = None

    class Config:
        orm_mode = True

