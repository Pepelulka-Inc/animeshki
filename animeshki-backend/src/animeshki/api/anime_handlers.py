import logging
import uuid

<<<<<<< HEAD
=======
import jwt
>>>>>>> origin/main
from aiohttp import web
from pydantic import ValidationError
from sqlalchemy.future import select

<<<<<<< HEAD
from infrastructure.database.models import Anime
=======
from auth import SECRET_KEY
from infrastructure.database.models import Anime, Comments, UserAnimeStarsCount
>>>>>>> origin/main
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
<<<<<<< HEAD
=======
                mal_id=anime.mal_id,
>>>>>>> origin/main
            )

            await session.commit()
            return web.json_response(pydantic_model.model_dump())
    except Exception as e:
        _logger.warning(f"Can't give anime by id: {e}")
        return res_error("Something went wrong")


<<<<<<< HEAD
=======
async def post_animes_by_ids(request: web.Request) -> web.Response:
    """
    /POST anime/get/many

    Получение списка аниме по списку айди
    """
    data = await request.json()
    ids = data["ids"]
    try:
        async with Session() as session:
            result = await session.execute(select(Anime).where(Anime.anime_id.in_(ids)))
            animes = result.scalars().all()
            result = {}
            for anime in animes:
                pydantic_model = AnimeModel(
                    anime_id=str(anime.anime_id),
                    title=anime.title,
                    description=anime.description,
                    picture_minio_path=anime.picture_minio_path,
                    mal_id=anime.mal_id,
                )
                result[str(anime.anime_id)] = pydantic_model.model_dump()

            await session.commit()
            return web.json_response(result)
    except Exception as e:
        _logger.warning(f"Can't give animes by ids: {e}")
        return res_error("Something went wrong")


>>>>>>> origin/main
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
<<<<<<< HEAD
=======
                mal_id=anime_create.mal_id,
>>>>>>> origin/main
            )

            session.add(new_anime)

            await session.commit()
    except Exception as e:
        _logger.warning(f"Can't add anime: {e}")
        return res_error("Something went wrong")

    return web.json_response({"anime_id": str(new_anime_id)})
<<<<<<< HEAD
=======


async def get_comments_for_anime_by_id(request: web.Request) -> web.Response:
    """
    /GET anime/{anime_id}/comments

    Получаем все комментарии для анимешки
    """

    anime_id = request.match_info["anime_id"]
    _logger.info(f"Fetching comments for anime ID: {anime_id}")

    try:
        anime_id = uuid.UUID(anime_id)
        async with Session() as session:
            result = await session.execute(
                select(Comments.username, Comments.body).where(
                    Comments.anime_id == anime_id
                )
            )
            comments = result.fetchall()
            if comments is None:
                comments_list = []
            else:
                comments_list = [
                    {
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
    except ValueError:
        return web.json_response({"error": "Invalid anime ID format."}, status=400)
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
        anime_id = uuid.UUID(anime_id)
        token = request.cookies.get("access_token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")
        data = await request.json()
        comment_text = data["text"]

        if not comment_text or not username:
            return web.json_response(
                {"error": "Text and user are required."}, status=400
            )

        _logger.info(f"Adding comment for anime ID: {anime_id} by user: {username}")

        async with Session() as session:
            new_comment = Comments(
                anime_id=anime_id, body=comment_text, username=username
            )

            session.add(new_comment)
            await session.commit()

            _logger.info(f"Comment added for anime ID: {anime_id} by user: {username}")
            return web.json_response({"msg": "Comment added successfully."}, status=201)

    except ValueError:
        return web.json_response({"error": "Invalid anime ID format."}, status=400)
    except Exception as e:
        _logger.error(f"Error adding comment for anime ID {anime_id}: {e}")
        return web.json_response({"error": str(e)}, status=500)


async def rate_anime(request: web.Request) -> web.Response:
    """
    /POST anime/{anime_id}/rate

    Оценка фильма по 10-балльной шкале
    """

    anime_id = request.match_info["anime_id"]

    try:
        anime_id = uuid.UUID(anime_id)
        data = await request.json()
        rating = data.get("rating")

        if rating is None or not (1 <= rating <= 10):
            return web.json_response(
                {"error": "Rating must be an integer between 1 and 10."}, status=400
            )

        token = request.cookies.get("access_token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("username")

        _logger.info(
            f"Rating anime ID: {anime_id} by user: {username} with rating: {rating}"
        )

        async with Session() as session:
            new_rating = UserAnimeStarsCount(
                anime_id=anime_id, username=username, stars=rating
            )

            session.add(new_rating)
            await session.commit()

            _logger.info(f"Rating added for anime ID: {anime_id} by user: {username}")
            return web.json_response({"msg": "Rating added successfully."}, status=201)

    except ValueError:
        return web.json_response({"error": "Invalid anime ID format."}, status=400)
    except jwt.ExpiredSignatureError:
        return web.json_response({"error": "Token has expired."}, status=401)
    except jwt.InvalidTokenError:
        return web.json_response({"error": "Invalid token."}, status=401)
    except Exception as e:
        _logger.error(f"Error adding rating for anime ID {anime_id}: {e}")
        return web.json_response({"error": str(e)}, status=500)


async def get_anime_rates(request: web.Request) -> web.Response:
    """
    /GET anime/{anime_id}/rate

    Получение всех оценок фильма
    """

    anime_id = request.match_info["anime_id"]

    try:
        anime_id = uuid.UUID(anime_id)

        async with Session() as session:
            result = await session.execute(
                select(UserAnimeStarsCount).where(
                    UserAnimeStarsCount.anime_id == anime_id
                )
            )
            ratings = result.fetchall()

            ratings_list = [
                {"username": rating.username, "rating": rating.stars}
                for rating in ratings
            ]

            return web.json_response({"ratings": ratings_list}, status=200)

    except ValueError:
        return web.json_response({"error": "Invalid anime ID format."}, status=400)
    except Exception as e:
        _logger.error(f"Error retrieving ratings for anime ID {anime_id}: {e}")
        return web.json_response({"error": str(e)}, status=500)
>>>>>>> origin/main
