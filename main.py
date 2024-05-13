from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title='Trading App'
)

fake_users = [
    {'id': 1, 'role': 'admin', 'name': 'Bob'},
    {'id': 2, 'role': 'investor', 'name': 'Alex'},
    {'id': 3, 'role': 'traider', 'name': 'Nasty'}
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


class User(BaseModel):
    """Класс Пользователь"""
    id: int
    role: str
    name: str


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
