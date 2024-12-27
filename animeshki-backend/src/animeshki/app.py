from aiohttp import web

from api.anime_handlers import (
    get_anime_by_id,
    add_anime,
    post_animes_by_ids,
    get_comments_for_anime_by_id,
    set_comment_for_anime_by_id,
    rate_anime,
    get_anime_rates,
)
from api.user_handlers import get_favorites, add_favorite, get_user_id_by_username
from infrastructure.database.engine import init_db_and_tables


async def on_startup(app):
    await init_db_and_tables()


app = web.Application()
app.router.add_post("/{username}/favorites/get", get_favorites)
app.router.add_post("/{username}/favorites/add", add_favorite)
app.router.add_get("/get_user_id/{username}", get_user_id_by_username)

app.router.add_get("/anime/get/{anime_id}", get_anime_by_id)
app.router.add_post("/anime/get/many", post_animes_by_ids)
app.router.add_post("/anime/add", add_anime)
app.router.add_get("/anime/{anime_id}/comments", get_comments_for_anime_by_id)
app.router.add_post("/anime/{anime_id}/comments", set_comment_for_anime_by_id)
app.router.add_post("/anime/{anime_id}/rate", rate_anime)
app.router.add_get("/anime/{anime_id}/rate", get_anime_rates)
app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(app, port=9002)
