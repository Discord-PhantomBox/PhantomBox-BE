
from fastapi import APIRouter, Response, Request

from service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login/google")
async def google_login_url(request : Request):
    origin = request.headers.get("origin")
    url_response = await auth_service.show_url(origin)
    return url_response

@router.get("/login/google/callback")
async def google_login_callback(code : str, state : str):
    redirect_response = await auth_service.login(code, state)
    return redirect_response
