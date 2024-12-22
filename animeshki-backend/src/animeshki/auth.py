import os
import asyncio
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
ACCESS_TOKEN_EXPIRE_DAYS = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    data: Dict[str, datetime], expires_delta: timedelta = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(days=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: Dict[str, datetime]) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def check_credentials_admin(role: str):
    """
    Декоратор проверяющий привелегию, вешается на все админские ручки
    :param role:
    :return:
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: web.Request) -> web.Response:
            data = await request.json()
            username = data["username"]
            async with Session() as session:
                res = await session.execute(
                    select(User.role).where(User.username == username)
                )
                role = res.scalar_one_or_none()
                logger.info(f"role: {role}")
                if role == "user":
                    return web.json_response({"msg": "Access denied"}, status=401)
            return await func(request)

        return wrapper

    return decorator


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
        print(user_data)

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

        access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        access_token = create_access_token(
            data={"sub": username, "role": user_data.role},
            expires_delta=access_token_expires,
        )
        refresh_token = create_refresh_token(data={"sub": username})
        logger.info(f"Пользователь успешно вошел в систему: {username}")
        return web.json_response(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        )


@check_credentials_admin("admin")
async def refresh_access_token(request: web.Request) -> web.Response:
    """
    /POST refresh

    Обновление access_token по refresh_token
    """
    data = await request.json()
    refresh_token = data["refresh_token"]

    if not refresh_token:
        return web.json_response({"msg": "Refresh token is required"}, status=400)

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]

        if username is None:
            raise jwt.InvalidTokenError("Invalid token")

        access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        new_access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )

        return web.json_response(
            {"access_token": new_access_token, "refresh_token": refresh_token}
        )

    except jwt.InvalidTokenError:
        return web.json_response({"msg": "Invalid refresh token"}, status=401)


app = web.Application()
app.router.add_post("/register", register)
app.router.add_post("/login", login)
app.router.add_post("/refresh", refresh_access_token)

if __name__ == "__main__":
    asyncio.run(init_db_and_tables())
    web.run_app(app, port=9000)
