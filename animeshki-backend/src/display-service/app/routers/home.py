from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime
import jwt
import os
from dotenv import load_dotenv
from token_work import verify_access_token


load_dotenv()
SECRET_KEY = str(os.getenv("SECRET_KEY"))

ALGORITHM = "HS256"

template = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get(path='/')
async def show_register_page(request: Request):
    token = request.cookies.get("access_token")
    if verify_access_token(token):
        return template.TemplateResponse("home.html", {"request": request})
    else:
        return