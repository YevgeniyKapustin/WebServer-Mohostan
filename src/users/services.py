import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from src.config import SECRET_KEY, TOKEN_URL, JWT_ALGORITHM
from src.database import session
from src.users.models import User
from src.users.utils import get_string_hash, verify_password
from src.users.schemas import UserCreate


async def create_user(user: UserCreate) -> bool:
    """Создание пользователя."""
    if not await get_user_by_email(user.email):
        session.add(
            User(
                email=user.email,
                hashed_password=await get_string_hash(user.password),
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


async def authenticate_user(email: str, password: str) -> User | None:
    """Определение подлинности пользователя"""
    user = await get_user_by_email(email)
    if not user:
        return None
    if not await verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user_by_token(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl=TOKEN_URL))

) -> User | None:
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail='Вы не авторизованы',
    )

    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[JWT_ALGORITHM]
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
