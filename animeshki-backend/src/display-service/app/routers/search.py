from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from token_work import verify_access_token, refresh_access_token, get_username_by_token

template = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get(path='/search')
async def show_register_page(request: Request, query: str):
    token = request.cookies.get("access_token")
    print(query)
    if verify_access_token(token):
        # тоже в респонз пихнуть надо инфу про аниме
        return template.TemplateResponse("search.html", {"request": request})
    else:
        return
    
async def get_anime_list(query: str):
    # тут надо обратиться к моему сервису и получить список аниме
    # потом надо обратиться к другим сервисам и получить инфу про них
    return