import logging
import uuid

from aiohttp import web
from pydantic import ValidationError
from sqlalchemy.future import select

from infrastructure.database.models import Anime, Comments
from infrastructure.database.engine import Session
from domain.anime import AnimeModel, AnimeCreateModel

_logger = logging.getLogger(__name__)


def res_error(msg):
    return web.json_response({"msg": msg}, status=400)


def res_not_found():
    return web.json_response({"msg": "Not found"}, status=404)


async def get_anime_by_id(request: web.Request) -> web.Response:
    """
    /GET anime/{anime_id}

    Получение аниме по айди
    """
    anime_id = request.match_info["anime_id"]
    try:
        async with Session() as session:
            result = await session.execute(
                select(Anime).where(Anime.anime_id == anime_id)
            )
            anime = result.scalar_one_or_none()
            if anime is None:
                return res_not_found()
            pydantic_model = AnimeModel(
                anime_id=str(anime.anime_id),
                title=anime.title,
                description=anime.description,
                picture_minio_path=anime.picture_minio_path,
            )

            await session.commit()
            return web.json_response(pydantic_model.model_dump())
    except Exception as e:
        _logger.warning(f"Can't give anime by id: {e}")
        return res_error("Something went wrong")


async def add_anime(request: web.Request) -> web.Response:
    """
    /POST anime/add

    Добавить новое аниме.
    Ждет на вход AnimeCreateModel.
    """
    data = await request.json()
    try:
        anime_create = AnimeCreateModel.model_validate(data)
    except ValidationError as e:
        return res_error(str(e))

    try:
        async with Session() as session:
            new_anime_id = uuid.uuid4()
            new_anime = Anime(
                anime_id=new_anime_id,
                title=anime_create.title,
                description=anime_create.description,
                picture_minio_path=anime_create.picture_minio_path,
            )

            session.add(new_anime)

            await session.commit()
    except Exception as e:
        _logger.warning(f"Can't add anime: {e}")
        return res_error("Something went wrong")

    return web.json_response({"anime_id": str(new_anime_id)})


async def get_comments_for_anime_by_id(request: web.Request) -> web.Response:
    """
    /GET anime/{anime_id}/comments

    Получаем все комментарии для анимешки
    """

    anime_id = request.match_info["anime_id"]
    _logger.info(f"Fetching comments for anime ID: {anime_id}")

    try:
        async with Session() as session:
            result = await session.execute(
                select(Comments).where(Comments.anime_id == anime_id)
            )
            comments = result.scalars().all()
            if comments is None:
                return res_not_found()
            comments_list = [
                {
                    "id": comment.comment_id,
                    "text": comment.body,
                    "user": comment.username,
                }
                for comment in comments
            ]

            _logger.info(
                f"Found {len(comments_list)} comments for anime ID: {anime_id}"
            )
            await session.commit()
            return web.json_response({"comments": comments_list})

    except Exception as e:
        _logger.error(f"Error fetching comments for anime ID {anime_id}: {e}")
        return web.json_response({"error": str(e)}, status=500)


async def set_comment_for_anime_by_id(request: web.Request) -> web.Response:
    """
    /POST anime/{anime_id}/comments

    Оставляем комментарий к анимешке
    """

    anime_id = request.match_info["anime_id"]
    try:
        data = await request.json()
        comment_text = data["text"]
        username = data["username"]

        if not comment_text or not username:
            return web.json_response(
                {"error": "Text and user are required."}, status=400
            )

        _logger.info(f"Adding comment for anime ID: {anime_id} by user: {username}")

        async with Session() as session:
            new_comment = Comments(anime_id=anime_id, body=comment_text, username=username)

            session.add(new_comment)
            await session.commit()

            _logger.info(f"Comment added for anime ID: {anime_id} by user: {username}")
            return web.json_response({"msg": "Comment added successfully."}, status=201)

    except Exception as e:
        _logger.error(f"Error adding comment for anime ID {anime_id}: {e}")
        return web.json_response({"error": str(e)}, status=500)
