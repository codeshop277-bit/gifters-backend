from fastapi import APIRouter, HTTPException, Depends
from database import gifts_mock, SessionLocal
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from schemas import GiftTemplate, GiftResponse
from models import Gifts, User
from sqlalchemy import func
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

#db: Session = Depends(get_db)
#Depends is a dependability in fastapi. It runs it first and pass get_db response as parameter
#db: Session means: “the variable db is expected to be of type Session.”
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

@router.get("/searchby/{column}/{value}")
def gifts_search(column: str, value: str, db:Session= Depends(get_db)):
    allowed_columns = {"id", "name", "brand", "size", "color", "user_id"}
    if column not in allowed_columns:
        raise HTTPException(status_code=404, detail=f"Column {column} not found")
    
    column_attr = getattr(Gifts, column) #fetches an attribute dynamically from an object similar to if column == "brand":
#     column_attr = Gifts.brand
# else if column == "color":
#     column_attr = Gifts.color

    result = db.query(Gifts).filter(func.lower(column_attr) == value.lower().strip()).all() #returns all data with same query (array)
    #strip() removes whitespaces
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    
    return result
    

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

@router.get("/search/{gift_id}", response_model=GiftResponse)
def get_gift_by_id(gift_id: int, db: Session = Depends(get_db)):
    gifts = db.query(Gifts).all()
    for gift in gifts:
        if gift.id == gift_id:
            return gift
        return {"error": f"Gift with id {gift_id} not found"}
    
@router.delete("/remove/{gift_id}")
def remove_gifts(gift_id: str, db: Session = Depends(get_db)):
    gift = db.query(Gifts).filter(Gifts.id == gift_id).first()
    if not gift:
        return {"Error": f"Gift with id {gift_id} not found"}
    db.delete(gift)
    db.commit()
    return {"Message": f"Gift with id {gift_id} has been deleted"}
    
@router.put("/update/{gift_id}")
def update_gift(gift_id: str, updated_gift: GiftCreate, db: Session = Depends(get_db)):
    gift = db.query(Gifts).filter(Gifts.id == gift_id).first()
    if not gift:
        raise HTTPException(status_code=404, detail=f"Gift with id {gift_id} not found")
    for key, value in updated_gift.model_dump().items():
        setattr(gift, key, value)

    db.commit()
    db.refresh(gift)
    return {gift}
    # for index, gift in enumerate(gifts_db):
    #     if gift.id == gift_id:
    #         new_gift = Gift(id = gift_id, **updated_gift.model_dump())
    #         gifts_db[index] = new_gift
    #         return new_gift
    # raise HTTPException(status_code=404, detail="Gift not found")

@router.patch("/patch/{gift_id}",)
def patch_gift(gift_id: str, patch: GiftPatch, db: Session = Depends(get_db)):
    gift = db.query(Gifts).filter(Gifts.id == gift_id).first()
    if not gift:
        raise HTTPException(status_code=404, detail="Gift not found")
    
    patch_data = patch.model_dump(exclude_unset=True)
    
    for key, value in patch_data.items():
        setattr(gift, key, value)

    db.commit()
    db.refresh(gift)

    return gift
    # for index, gift in enumerate(gifts_db):
    #     if gift.id == gift_id:
    #         new_data = patch.model_dump(exclude_unset=True)
    #         updated = gift.model_copy(update=new_data)
    #         gifts_db[index] = updated
    #         return updated
    # raise HTTPException(status_code=404, detail="Gift not found")

    #Claim GIFT
@router.get("/claim/{gift_id}/{user_id}")
def claim_gifts(gift_id: int, user_id: int, db: Session = Depends(get_db)):
    gift = db.query(Gifts).filter(Gifts.id == gift_id).first()
    if not gift:
        raise HTTPException(status_code=404, detail="Gift not found")
    if gift.claimed:
        raise HTTPException(status_code=400, detail="Gift already claimed")
    
    gift.claimed = True
    gift.user_id = user_id
    db.commit()
    db.refresh(gift)
    return gift