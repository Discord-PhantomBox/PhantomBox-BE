from urllib.request import Request

from fastapi import APIRouter, Response

from service import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login/google")
async def google_login_url():
    url_response = await auth_service.show_url()
    return url_response

@router.get("/login/google/callback")
async def google_login_callback(code : str):
    redirect_response = await auth_service.login(code)
    return redirect_response
