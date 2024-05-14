from fastapi_users.authentication import (AuthenticationBackend,
                                          CookieTransport, JWTStrategy)

cookie_transport = CookieTransport(cookie_name='bonds', cookie_max_age=3600)

# надо задать рандомную сложную строчку и хранить в .env
SECRET = "SECRET"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
