# jwt_util.py

from datetime import datetime, timedelta
from typing import Optional
import jwt
import os

# 환경변수 또는 config로 분리해도 좋습니다
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "asdmajskdnadjadoadjwpadnoadpiadnoadnanod")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 24

async def create_token(data: dict, type : str, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWT 토큰 발급
    :param data: 사용자 정보 (user_id, email 등)
    :param expires_delta: 만료 시간
    :return: JWT 문자열
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    to_encode.update({"typ": type})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_token(token: str) -> dict:
    """
    JWT 파싱 및 유효성 검사
    :param token: JWT 문자열
    :return: payload (user info)
    :raises: jwt.ExpiredSignatureError, jwt.InvalidTokenError
    """
    token = token.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")