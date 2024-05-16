from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers

from auth.base_config import auth_backend
from auth.models import User
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from auth.base_config import current_user
from operations import router_operation

# создание главного приложения
app = FastAPI(
    title='Trading App'
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
    prefix="/auth/jwt",
    tags=["Auth"],
)

# для регистрации
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)


@app.get('/protected-route')
def protected_route(user: User = Depends(current_user)):
    return f'Привет, {user.username}!'


@app.get('/unprotected-route')
def unprotected_route():
    return 'Привет, аноним!'
