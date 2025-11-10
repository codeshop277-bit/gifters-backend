from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from database import get_db
from models import Gifts, GiftsList

router = APIRouter(prefix="/share", tags=["Sharable links"])

from sqlalchemy.exc import SQLAlchemyError

@router.post("/{user_id}")
def create_sharable_links(user_id: int, db: Session = Depends(get_db)):
    try:
        new_list = GiftsList(user_id=user_id)
        db.add(new_list)
        db.commit()
        db.refresh(new_list)

        return {"url": f"http://localhost:3000/share/{new_list.share_token}"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/token/{token}")
def get_gifts(token: str, db: Session=Depends(get_db)):
    gift_list=db.query(GiftsList).filter(GiftsList.share_token == token).first()
    if not gift_list:
        raise HTTPException(status_code=401, detail="Token not found")
    print("gift_list", gift_list)
    gifts_of_user = db.query(Gifts).filter(Gifts.user_id == gift_list.user_id).all()
    print("gifts_of_user", gifts_of_user)
    return {"owner": gift_list.user_id, "gifts": gifts_of_user}
