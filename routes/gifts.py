from fastapi import APIRouter, HTTPException, Depends
from database import gifts_mock, SessionLocal
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from schemas import GiftTemplate, GiftResponse
from models import Gifts, User
import uuid

router = APIRouter(prefix="/gifts", tags=["gifts"]) #tags is for api documentation

class GiftCreate(BaseModel):
    name: str
    brand: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None

class Gift(GiftCreate):
    id: str

class GiftPatch(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None

class GiftDataBase(BaseModel):
    gifts: List[Gift]

gifts_db: list[Gift] = [Gift(id= '1', name='test', size='M', color="Red")]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Returns database
@router.get("")
def fetch_gifts():
    return gifts_db

@router.get("/searchby")
def gifts_search(brand: Optional[str] = None, max_price: Optional[int] = None):
    results = [
       gift  for gift in gifts_mock
       if (brand is None or gift["brand"].lower() == brand.lower()) and (max_price is None or gift["price"] <= max_price)
    ]
    return {"filtered": results}

@router.post("/add/{user_id}", response_model=GiftResponse)
def add_gift(user_id: int, gift: GiftTemplate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_gift = Gifts(
        name = gift.name,   
        brand = gift.brand,
        size = gift.size,
        color = gift.color,
        user_id = user_id
    )
    db.add(new_gift)
    db.commit()
    db.refresh(new_gift)
    #gifts_db.append(new_gift)
    return new_gift

@router.get("/search/{gift_id}")
def get_gift_by_id(gift_id: str):
    for gift in gifts_db:
        if gift.id == gift_id:
            return gift
        return {"error": f"Gift with id {gift_id} not found"}
    
@router.delete("/remove/{gift_id}")
def remove_gifts(gift_id: str):
    for gift in gifts_db:
        if gift.id == gift_id:
            gifts_db.remove(gift)
            return gifts_db
        return {"Error": f"Gift with id {gift_id} not found"}
    
@router.put("/update/{gift_id}", response_model=Gift)
def update_gift(gift_id: str, updated_gift: GiftCreate):
    for index, gift in enumerate(gifts_db):
        if gift.id == gift_id:
            new_gift = Gift(id = gift_id, **updated_gift.model_dump())
            gifts_db[index] = new_gift
            return new_gift
    raise HTTPException(status_code=404, detail="Gift not found")

@router.patch("/patch/{gift_id}", response_model=Gift)
def patch_gift(gift_id: str, patch: GiftPatch):
    for index, gift in enumerate(gifts_db):
        if gift.id == gift_id:
            new_data = patch.model_dump(exclude_unset=True)
            updated = gift.model_copy(update=new_data)
            gifts_db[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Gift not found")