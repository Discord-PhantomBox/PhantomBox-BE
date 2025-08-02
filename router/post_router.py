from fastapi import APIRouter, Depends

from depends.get_user import get_user
from model.post_model import PostRequest
from model.user_model import User
from service import post_service

router = APIRouter(prefix="/post", tags=["post"])

@router.post("/")
async def post(post_request : PostRequest, user: User = Depends(get_user)):
     post_response = await post_service.post(post_request, user)
     return post_response

@router.get("/")
async def get_posts():
     posts_response = await post_service.get_posts()
     return posts_response

@router.get("/{post_id:int}")
async def get_post(post_id: int):
     post_response = await post_service.get_post(post_id)
     return post_response

@router.get("/my")
async def get_my_posts(user : User = Depends(get_user)):
     posts_response = await post_service.get_my_posts(user)
     return posts_response

@router.patch("/{post_id:int}")
async def update_post(post_id: int, post_request : PostRequest):
     post_response = await post_service.update(post_id, post_request)
     return post_response

@router.delete("/{post_id:int}")
async def delete_post(post_id: int):
     post_response = await post_service.delete_post(post_id)
     return post_response
