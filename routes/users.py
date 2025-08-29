from fastapi import APIRouter, HTTPException
from database import users_list
from typing import Optional

router = APIRouter(prefix="/users", tags=["users"])

@router.get("")
def fetch_users_list():
    return users_list

@router.get("/search/{id}")
def search_user(id: int):
    result = next((user for user in users_list if user["id"] == id), None)
    if result is None:
        raise HTTPException(status_code=404, detail=f"User with id {id} does not exist")
    return {"user": result}