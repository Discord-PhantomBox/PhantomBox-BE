from fastapi import APIRouter, Depends
from depends.get_user import get_user
from model.user_model import User

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def my_user(user : User = Depends(get_user)):
    return user

