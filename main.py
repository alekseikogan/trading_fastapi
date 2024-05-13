from fastapi import FastAPI

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


@app.get('/users/{user_id}')
def get_user(user_id: int):
    return [user for user in fake_users if user.get('id') == user_id]


@app.get('/trades')
def get_trades(limit: int = 2, offset: int = 0):
    return fake_trades[offset:][:limit]
