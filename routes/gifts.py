from fastapi import APIRouter, HTTPException
from models import Gift, GiftCreate, GiftPatch
from database import gifts_db, gifts_mock
from typing import Optional
import uuid

router = APIRouter(prefix="/gifts", tags=["gifts"]) #tags is for api documentation

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

@router.post("/add", response_model=Gift)
def add_gift(gift: GiftCreate):
    new_gift= Gift(id= str(uuid.uuid4()), **gift.model_dump())
    gifts_db.append(new_gift)
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