import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from src.database import get_async_session
from src.services import execute_first_object
from src.config import SECRET_KEY, TOKEN_URL, JWT_ALGORITHM
from src.users.models import User
from src.users.utils import get_string_hash, verify_password
from src.users.schemas import UserCreate


async def create_user(session: AsyncSession, user: UserCreate) -> bool:
    """Создание пользователя."""
    if not await get_user_by_email(session, user.email):
        session.add(
            User(
                email=user.email,
                hashed_password=await get_string_hash(user.password),
            )
        )
        await session.commit()
        return True

    raise HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail='Пользователь с таким email уже существует',
    )


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    """Получение пользователя по email."""
    query = (
        select(User).
        where(User.email == email)
    )
    return await execute_first_object(session, query)


async def authenticate_user(
        session: AsyncSession, email: str, password: str

) -> User | None:
    """Определение подлинности пользователя"""
    user = await get_user_by_email(session, email)
    if not user:
        return None
    if not await verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user_by_token(
    session: AsyncSession = Depends(get_async_session),
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

    user = await get_user_by_email(session, email=email)

    if user is None:
        raise credentials_exception

    return user
