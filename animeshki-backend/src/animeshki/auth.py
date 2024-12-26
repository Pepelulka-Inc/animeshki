import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Dict

import jwt
import logging
from aiohttp import web
from dotenv import load_dotenv
from passlib.context import CryptContext
from sqlalchemy import select

from infrastructure.database.models import User
from infrastructure.database.engine import init_db_and_tables, Session


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
SECRET_KEY = str(os.getenv("SECRET_KEY"))

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    data: Dict[str, datetime], expires_delta: timedelta = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: Dict[str, datetime]) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def check_credentials_admin(func: Callable) -> Callable:
    """
    Декоратор проверяющий привелегию, вешается на все админские ручки
    """

    @wraps(func)
    async def wrapper(request: web.Request) -> web.Response:
        token = request.cookies.get("access_token")
        if not token:
            return web.json_response({"msg": "Token is missing"}, status=401)

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            role = payload.get("role")

            if role != "admin":
                return web.json_response({"msg": "Access denied"}, status=403)

        except jwt.ExpiredSignatureError:
            return web.json_response({"msg": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return web.json_response({"msg": "Invalid token"}, status=401)

        return await func(request)

    return wrapper


async def register(request: web.Request) -> web.Response:
    """
    /POST register

    Регистрация пользователя
    """
    data = await request.json()
    username = data["username"]
    password = data["password"]

    async with Session() as session:
        logger.info(f"Регистрация пользователя: {username}")

        result = await session.execute(select(User).where(User.username == username))
        user_data = result.scalar_one_or_none()

        if user_data:
            logger.warning(
                f"Попытка регистрации существующего пользователя: {username}"
            )
            return web.json_response({"msg": "User already exists"}, status=400)

        # TODO: надо будет продумать условия для паролей, и нужны ли они вообще
        if len(password) < 6:
            logger.warning(f"Попытка ввода невалидного пароля: {username}")
            return web.json_response(
                {"msg": "Please enter a password 6 symbols or longer"}, status=400
            )
        hashed_password = pwd_context.hash(password)
        role = "user"

        new_user = User(
            username=username,
            hashed_password=hashed_password,
            role=role,  # устанавливаем по дефолту
        )
        session.add(new_user)
        await session.commit()

        logger.info(f"Пользователь успешно зарегистрирован: {username}")

    return web.json_response({"msg": "User registered successfully"})


async def login(request: web.Request) -> web.Response:
    """
    /POST login

    Вход пользователя в систему, выдаются токены
    """
    data = await request.json()
    username = data["username"]
    password = data["password"]

    async with Session() as session:
        logger.info(f"Попытка входа пользователя: {username}")

        result = await session.execute(select(User).where(User.username == username))
        user_data = result.scalar_one_or_none()

        if not user_data or not pwd_context.verify(password, user_data.hashed_password):
            logger.warning(f"Неверные учетные данные для пользователя: {username}")
            return web.json_response(
                {"msg": "Invalid username or password"}, status=400
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username, "role": user_data.role},
            expires_delta=access_token_expires,
        )
        refresh_token = create_refresh_token(data={"sub": username})

        response = web.json_response({"msg": "User login successfully"})
        response.set_cookie("access_token", access_token, httponly=True)
        response.set_cookie("refresh_token", refresh_token, httponly=True)

        logger.info(f"Пользователь успешно вошел в систему: {username}")
        return response


async def refresh_access_token(request: web.Request) -> web.Response:
    """
    /POST refresh

    Refresh access token using refresh token from cookies
    """
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        return web.json_response({"msg": "Refresh token is required"}, status=400)

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise jwt.InvalidTokenError("Invalid token")

        if "exp" in payload and datetime.now() > datetime.fromtimestamp(payload["exp"]):
            return web.json_response({"msg": "Refresh token has expired"}, status=401)

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )

        response = web.json_response({"msg": "Access token refreshed"})
        response.set_cookie("access_token", new_access_token, httponly=True)

        return response

    except jwt.ExpiredSignatureError:
        return web.json_response({"msg": "Refresh token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return web.json_response({"msg": "Invalid refresh token"}, status=401)


async def on_startup(app):
    await init_db_and_tables()


app = web.Application()
app.router.add_post("/api/v1/register", register)
app.router.add_post("/api/v1/login", login)
app.router.add_post("/api/v1/refresh", refresh_access_token)

app.on_startup.append(on_startup)

if __name__ == "__main__":
    # asyncio.run(init_db_and_tables())
    web.run_app(app, port=9000)
