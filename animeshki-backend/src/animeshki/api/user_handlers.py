import logging

from aiohttp import web
from sqlalchemy.future import select

from infrastructure.database.models import Favorites, User
from infrastructure.database.engine import Session


_logger = logging.getLogger(__name__)


async def get_user_id_by_username(request: web.Request) -> web.Response:
    """
    /GET /get_user_id/{username}

    Получение user_id по username
    """
    username = request.match_info["username"]
    _logger.info(f"Fetching favorites for user: {username}")
    async with Session() as session:
        result = await session.execute(
            select(User).where(User.username == username)
        )
        record = result.scalars().first()

        if record is None:
            return web.json_response({"user_id": None})
        return web.json_response({"user_id": int(record.user_id)})

async def get_favorites(request: web.Request) -> web.Response:
    """
    /GET {username}/favorites

    Получение избранных аниме пользователя
    """
    username = request.match_info["username"]
    _logger.info(f"Fetching favorites for user: {username}")
    async with Session() as session:
        result = await session.execute(
            select(Favorites).where(Favorites.username == username)
        )
        favorites = result.scalars().all()

        favorite_anime_ids = [fav.anime_id for fav in favorites]
        _logger.info(f"Found {len(favorite_anime_ids)} favorites for user: {username}")
        return web.json_response({"favorites": favorite_anime_ids})


async def add_favorite(request: web.Request) -> web.Response:
    """
    /POST {username}/favorites

    Добавление аниме в избранное
    """
    data = await request.json()
    username = request.match_info["username"]

    anime_id = data["anime_id"]

    if not username or not anime_id:
        _logger.warning("Username or anime_id not provided")
        return web.json_response(
            {"msg": "Username and anime_id are required"}, status=400
        )

    _logger.info(f"Adding favorite anime (ID: {anime_id}) for user: {username}")
    async with Session() as session:
        existing_favorite = await session.execute(
            select(Favorites).where(
                User.username == username, User.anime_id == anime_id
            )
        )

        if existing_favorite.scalars().first() is not None:
            _logger.warning(
                f"Anime ID {anime_id} is already in favorites for user: {username}"
            )
            return web.json_response({"msg": "Anime already in favorites"}, status=400)

        new_favorite = Favorites(username=username, anime_id=anime_id)
        session.add(new_favorite)
        await session.commit()

        _logger.info(f"Anime ID {anime_id} added to favorites for user: {username}")
        return web.json_response({"msg": "Anime added to favorites"}, status=201)
