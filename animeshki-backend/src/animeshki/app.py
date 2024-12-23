from aiohttp import web

from api.user_handlers import get_favorites, add_favorite
from infrastructure.database.engine import init_db_and_tables


async def on_startup(app):
    await init_db_and_tables()


app = web.Application()
app.router.add_post("/favorites/get", get_favorites)
app.router.add_post("/favorites/add", add_favorite)

app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(app, port=9002)
