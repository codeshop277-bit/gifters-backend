from pydantic import BaseModel
from typing import List, Optional

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