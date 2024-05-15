from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f'postgresql+asyncpg://%{DB_USER}s:%{DB_PASS}s@%{DB_HOST}s:%{DB_PORT}s/%{DB_NAME}s'
# Метаданные для базы, о таблицах
Base: DeclarativeMeta = declarative_base()


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
