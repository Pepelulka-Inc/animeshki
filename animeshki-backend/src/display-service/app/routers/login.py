from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

template = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get(path='/login')
async def show_register_page(request: Request):
    return template.TemplateResponse("login.html", {"request": request})