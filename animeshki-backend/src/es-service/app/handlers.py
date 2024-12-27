from aiohttp.web import Request, Response, json_response

from elastic import get_elastic_client


async def search_anime(request: Request) -> Response:
    """
    /GET search

    Поиск анимешки в списке анимешек
    """
    search_query = request.query.get("search_query")
    es_client = get_elastic_client()
    response = await es_client.search(search_query=search_query)
    return json_response(response)

async def add_animes(request: Request) -> Response:
    """
    /POST add

    Добавление анимешки
    """
    data = await request.json()
    es_client = get_elastic_client()
    try:
        await es_client.add(data)
    except Exception as e:
        return json_response({"msg": str(e)}, status=400)
    return json_response({"msg": "ok"})