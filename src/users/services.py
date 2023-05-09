from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from src.config import SECRET_KEY, ALGORITHM, TOKEN_URL
from src.database import session
from src.users import schemas
from src.users.models import User
from src.users.utils import get_string_hash, verify_password


async def create_user(user: schemas.UserCreate) -> bool:
    """Создание пользователя."""
    a = await get_user_by_email(user.email)
    if not await get_user_by_email(user.email):
        session.add(
            User(
                email=user.email,
                hashed_password=get_string_hash(user.password),
            )
        )
        session.commit()
        return True
    raise HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail='Пользователь с таким email уже существует',
    )


async def get_user_by_email(email: str) -> User:
    """Получение пользователя по email."""
    return (
        session.query(User).
        where(User.email == email).
        first()
    )


async def authenticate_user(email: str, password: str) -> Optional[User]:
    """Определение подлинности пользователя"""
    user = await get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user_by_token(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl=TOKEN_URL))
):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail='Вы не авторизованы',
    )
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.DecodeError:
        raise credentials_exception
    user = await get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user
