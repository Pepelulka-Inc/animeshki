from datetime import datetime
import jwt
import os
from dotenv import load_dotenv
from fastapi import Request
import httpx
from starlette.templating import _TemplateResponse

load_dotenv()
SECRET_KEY = str(os.getenv("SECRET_KEY"))

ALGORITHM = "HS256"

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except Exception as e:
        print(str(e))
        return False

async def refresh_access_token(request: Request):
    url = "http://auth-service:9000/api/v1/refresh"
    cookies = {
        "access_token": request.cookies.get("access_token"),
        "refresh_token": request.cookies.get("refresh_token")
    }
    async with httpx.AsyncClient() as client:
        return await client.post(url, cookies=cookies)
    
async def update_response_with_refreshed_access_token(response: _TemplateResponse, request: Request):
    other_service_response = await refresh_access_token(request)
    refreshed_access_token = other_service_response.cookies.get("access_token")
    response.set_cookie("access_token", refreshed_access_token)
    return response

def get_username_by_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")