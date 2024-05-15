import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Предоставляет основные поля и валидацию."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Предназначен для регистрации пользователей,
       которые состоят из обязательных email и password полей."""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Обновление профиля пользователя, которое добавляет необязательное password поле."""
    pass