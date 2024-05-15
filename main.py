from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from fastapi_users import FastAPIUsers
from pydantic import BaseModel, Field, ValidationError

from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead

app = FastAPI(
    title='Trading App'
)
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# создание роутеров
# для авторизации
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

# для регистрации
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f'Привет, {user.username}!'


@app.get('/unprotected-route')
def protected_route():
    return f'Привет, аноним!'


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'message': exc.errors()})
    )


@app.exception_handler(ValidationError)
async def response_validation_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'message': exc.errors()})
    )


fake_users = [
    {'id': 1, 'role': 'admin', 'name': ['John', 'Doe']},
    {'id': 2, 'role': 'investor', 'name': 'Alex'},
    {'id': 3, 'role': 'traider', 'name': 'Nasty', 'degree': [
        {'id': 1, 'created_at': '2024-05-11T02:55:59', 'type_degree': 'expert'}
    ]}
]

fake_trades = [
    {'id': 1, 'user_id': 2, 'side': 'buy', 'currency': 'BTC', 'price': 200, 'amount': 2.12},
    {'id': 2, 'user_id': 3, 'side': 'sell', 'currency': 'LUNA', 'price': 5, 'amount': 200.00},
    {'id': 3, 'user_id': 1, 'side': 'sell', 'currency': 'BTC', 'price': 150, 'amount': 4.00},
    {'id': 4, 'user_id': 1, 'side': 'buy', 'currency': 'EFT', 'price': 50, 'amount': 10.00},
]


class Trade(BaseModel):
    """Класс Сделка"""
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float = Field(g=0)


class DegreeType(Enum):
    noob = 'noob'
    middle = 'middle'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    """Класс Пользователь"""
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@app.get('/users/{user_id}', response_model=List[User])
def get_user(user_id: int):
    """Получение данных пользователя по id"""
    return [user for user in fake_users if user.get('id') == user_id]


@app.get('/trades')
def get_trades(limit: int = 2, offset: int = 0):
    """Получение истории трейдов"""
    return fake_trades[offset:][:limit]


@app.post('/users/{user_id}')
def change_user_name(user_id: int, new_name: str):
    """Изменение имени пользователя по id"""
    current_user = list(filter(lambda user: user.get('id') == user_id, fake_users))
    if current_user:
        current_user[0]['name'] = new_name
        return {'status': 200, 'data': f'Имя пользователя успешно изменено на {new_name}'}
    return {'status': 404, 'data': f'Пользователь с id={user_id} не найден.'}


@app.post('/trades')
def add_trades(trade: List[Trade]):
    """Добавление данных сделки"""
    fake_trades.extend(trade)
    return {'status': 200, 'data': trade}
