from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from token_work import verify_access_token, refresh_access_token, get_username_by_token, update_response_with_refreshed_access_token
import httpx

template = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get(path='/search')
async def show_search_page(request: Request, query: str):
    token = request.cookies.get("access_token")
    anime_list = await get_anime_list(query)
    if verify_access_token(token):
        return template.TemplateResponse("search.html", {"request": request, "anime_list": anime_list})
    else:
        new_response = template.TemplateResponse("home.html", {"request": request, "anime_list": anime_list})
        return await update_response_with_refreshed_access_token(response=new_response, request=request)
    
async def get_anime_list(query: str):
    url = f"http://es-service:8001/search?search_query={query}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        search_response_serialized = response.json()
    id_list = [item['id'] for item in search_response_serialized]
    url = "http://main-service:9002/anime/get/many"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"ids": id_list})
        search_response_serialized = response.json()
    return search_response_serialized