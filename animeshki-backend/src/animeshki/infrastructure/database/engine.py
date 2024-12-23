import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from infrastructure.database.models import Base


load_dotenv()
DB_URL = str(os.getenv("DATABASE_URL"))
engine = create_async_engine(DB_URL, echo=True)


Session = async_sessionmaker(engine)


async def init_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
