import asyncio
import logging

import bcrypt

from aiohttp import web
from aiohttp.abc import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response


user_db = {}
logging.basicConfig(level=logging.INFO)


async def index(request: Request) -> Response:
    return Response(status=200, text="It works!")


async def register(request: Request) -> Response:
    try:
        data = await request.json()
        username = data["username"]
        password = data["password"]

        if username in user_db:
            return Response(status=400, text="User already exist")

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user_db[username] = hashed_password

        logging.info(f"User {username} register successfully")
        return Response(status=200, text="User registered")
    except Exception as e:
        logging.error(f"Error during registration: {e}")
        return Response(status=500, text="Server error")


async def login(request: Request) -> Response:
    try:
        data = await request.json()
        username = data["username"]
        password = data["password"]

        if username not in user_db:
            return Response(status=400, text="User not found")

        hashed_password = user_db[username]
        if not bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            return Response(status=400, text="Invalid password")

        logging.info(f"User {username} login successfully")
        return Response(status=200, text="Login successful")

    except Exception as e:
        logging.error(f"Error during login: {e}")
        return Response(status=500, text="Server error")


async def users(request: Request) -> Response:
    if user_db:
        return Response(status=200, text=f"Users: {user_db.keys()}")
    else:
        return Response(status=500, text="Users not found, you can create it")


async def init_app() -> Application:
    _app = web.Application()
    _app.router.add_post("/register", register)
    _app.router.add_post("/login", login)
    _app.router.add_post("/users", users)
    _app.router.add_get("/", index)

    return _app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app())
    web.run_app(app, host="127.0.0.1", port=8080)
