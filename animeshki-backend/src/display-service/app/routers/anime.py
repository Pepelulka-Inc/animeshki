from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from token_work import verify_access_token, get_username_by_token, update_response_with_refreshed_access_token

template = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get(path='/anime')
async def show_anime_page(request: Request):
    token = request.cookies.get("access_token")
    if verify_access_token(token):
        # вот тут надо как-то в респонз пихнуть инфу про аниме
        return template.TemplateResponse("anime.html", {"request": request})
    else:
        new_response = template.TemplateResponse("anime.html", {"request": request})
        return await update_response_with_refreshed_access_token(response=new_response, request=request)