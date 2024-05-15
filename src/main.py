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


@app.get('/protected-route')
def protected_route(user: User = Depends(current_user)):
    return f'Привет, {user.username}!'


@app.get('/unprotected-route')
def unprotected_route():
    return 'Привет, аноним!'


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
