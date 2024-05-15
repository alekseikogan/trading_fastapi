from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Предоставляет основные поля и валидацию."""
    id: int
    email: str
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    """Предназначен для регистрации пользователей,
       которые состоят из обязательных email и password полей."""
    username: str
    email: str
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    """Обновление профиля пользователя, которое добавляет необязательное password поле."""
    pass
