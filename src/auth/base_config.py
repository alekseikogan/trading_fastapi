# from datetime import datetime
from typing import AsyncGenerator

from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)
from sqlalchemy.ext.asyncio import AsyncSession

from config import SECRET_AUTH
from src.database import User

from .manager import get_user_manager

# from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
# from sqlalchemy.orm import DeclarativeBase

cookie_transport = CookieTransport(
    cookie_name='bonds',
    cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

#  ТО ЧТО НИЖЕ НАДО ПРОВЕРИТЬ И ВОЗМОЖНО УДАЛИТЬ

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
