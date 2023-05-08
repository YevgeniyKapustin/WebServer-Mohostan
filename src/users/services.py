from typing import Optional

from src.database import session
from src.users import schemas
from src.users.models import User
from src.users.utils import get_string_hash

from users.utils import verify_password


async def create_user(user: schemas.UserCreate) -> bool:
    """Создание пользователя."""
    session.add(
        User(
            email=user.email,
            hashed_password=get_string_hash(user.password),
        )
    )
    session.commit()
    return True


async def get_user_by_email(email: str) -> User:
    """Получение пользователя по email."""
    return (
        session.query(User).
        where(User.email == email).
        first()
    )


async def authenticate_user(email: str, password: str) -> Optional[User]:
    user = await get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
