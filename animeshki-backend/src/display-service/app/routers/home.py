from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime
import jwt
import os
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = str(os.getenv("SECRET_KEY"))

ALGORITHM = "HS256"

template = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get(path='/')
async def show_register_page(request: Request):
    token = request.cookies.get("access_token")
    print(token)
    if await verify_access_token(token):
        return template.TemplateResponse("home.html", {"request": request})
    else:
        return

async def verify_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    expire = payload.get("exp")
    if datetime.fromtimestamp(expire) < datetime.now():
        return False
    return True
