from functools import wraps
from typing import Optional
from fastapi import Request, HTTPException

from model.user_model import User
from service import user_service
from util import jwt_util

async def get_user(request: Request) -> User:
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="인증 실패: 토큰 필요")
    token_value = token[7:]
    decoded_token = await jwt_util.decode_token(token_value)
    print(decoded_token)
    user_id = decoded_token.get("user_id")
    user = await user_service.get_user_by_id(user_id)
    return user
