from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from src.users.models import User


def trust_check(current_user: User) -> bool:

    if not current_user.is_trusted:
        raise HTTPException(
            HTTP_401_UNAUTHORIZED,
            detail='Вы не являетесь доверенным пользователем'
        )
    return True
