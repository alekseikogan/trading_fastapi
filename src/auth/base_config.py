from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)

from config import SECRET_AUTH

from .manager import get_user_manager
from .models import User

cookie_transport = CookieTransport(
    cookie_name='bonds',
    cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    """Создание стратегии токена."""
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600)


# подытоживание стратегии и транспорта
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# позволит генерировать фактические маршруты API
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# получение текущего пользователя
# можно ставить фильтры н-р active=True
current_user = fastapi_users.current_user()
