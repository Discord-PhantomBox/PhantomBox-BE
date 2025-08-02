import os
from dotenv import load_dotenv
from fastapi import Response
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import google.oauth2.id_token
from starlette.responses import RedirectResponse
from util import jwt_util
from model.auth_model import GoogleUrlResponse
from dao.mysql_dao import mysql_dao

load_dotenv()

REDIRECT_URI = "https://a08377b5e54d.ngrok-free.app/auth/login/google/callback"
client_config = {
    "web": {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "redirect_uri": REDIRECT_URI,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "grant_type": "authorization_code"
    }
}

SCOPES = ['openid',
          'https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile']

flow = Flow.from_client_config(client_config, scopes=SCOPES)
flow.redirect_uri = REDIRECT_URI

async def show_url() -> GoogleUrlResponse:
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline', include_granted_scopes='true')
    return GoogleUrlResponse(url=auth_url)


async def __saved_user(user_email, user_name):
    sql = "insert into user(name, email) values (%s, %s)"
    user_id = mysql_dao.execute_update(sql, (user_name, user_email))
    return user_id


ACCESS_TOKEN = "access_token"
REFRESH_TOKEN = "refresh_token"

async def login(code : str) -> RedirectResponse:
    flow.fetch_token(code=code)
    credentials = flow.credentials
    auth_req = google.auth.transport.requests.Request()
    id_info = google.oauth2.id_token.verify_oauth2_token(
        credentials.id_token, auth_req, client_config["web"]["client_id"]
    )

    user_email = id_info.get("email")
    user_name = id_info.get("name")

    user_id = await __saved_user(user_email, user_name)
    # jwt issue
    token_info = {
        "user_id" : user_id,
        "email" : user_email,
        "name" : user_name,
    }
    access_token = await jwt_util.create_token(token_info, ACCESS_TOKEN)
    refresh_token = await jwt_util.create_token(token_info, REFRESH_TOKEN)

    redirect = RedirectResponse(
        url=f"http://10.10.5.252:3000/login/success?access_token={access_token}"
    )
    print(f"access_token : {access_token}")
    redirect.set_cookie("refresh_token", refresh_token)
    return redirect