from datetime import datetime, timedelta

from jwt import encode
from passlib.context import CryptContext

from src.config import Settings

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие пароля хэшированному паролю."""
    return password_context.verify(plain_password, hashed_password)


async def get_string_hash(string: str) -> str:
    """Возвращает хэш от строки."""
    return password_context.hash(string)


async def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
):
    """Создание JWT токена"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update(
        {
            "exp": expire,
        }
    )

    encoded_jwt = encode(
        to_encode, Settings().SECRET_KEY, algorithm=Settings().JWT_ALGORITHM
    )
    return encoded_jwt
