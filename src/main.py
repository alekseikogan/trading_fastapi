from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers
from redis import asyncio as aioredis

from auth.base_config import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserCreate, UserRead
from operations.routers import router as router_operation
from pages.router import router as router_pages
from tasks.router import router as router_tasks

# создание главного приложения
app = FastAPI(
    title='Trading App'
)

app.mount('/static', StaticFiles(directory='static'), name='static')

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=['Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers', 'Access-Control-Allow-Origin',
                   'Authorization'],
)

# позволит генерировать фактические маршруты API
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# создание роутеров
# для авторизации
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['Auth'],
)

# для регистрации
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['Auth'],
)

app.include_router(router_operation)
app.include_router(router_tasks)
app.include_router(router_pages)


@app.on_event('startup')
async def startup_event():
    redis = aioredis.from_url('redis://localhost',
                              encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


# @app.get('/protected-route')
# def protected_route(user: User = Depends(current_user)):
#     return f'Привет, {user.username}!'


# @app.get('/unprotected-route')
# def unprotected_route():
#     return 'Привет, аноним!'
