from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from token_work import verify_access_token, refresh_access_token, get_username_by_token

template = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get(path='/')
async def show_register_page(request: Request):
    token = request.cookies.get("access_token")
    if verify_access_token(token):
        # вот тут надо как-то в респонз пихнуть инфу про аниме
        return template.TemplateResponse("home.html", {"request": request})
    else:
        return
    

async def get_recomended_anime_ids(token: str):
    username = get_username_by_token(token)
    # тут надо отправить запрос на получение рекомендованных аниме и получить дикт с ключом айди и значением описанием
    # тут надо по списку айди получить... а я хуй знает
    # смотри по ручкам. По факту надо получить айди рекомендованных аниме через сервис рекомендаций, а потом подтянуть информацию об этих аниме
    # т.е. название аниме, путь к картинке и рейтинг