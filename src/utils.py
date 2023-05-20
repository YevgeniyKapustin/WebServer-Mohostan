from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from src.users.models import User


def trust_check(current_user: User) -> bool:

    if not current_user.is_trusted:
        raise HTTPException(
            HTTP_403_FORBIDDEN,
            detail='Вы не являетесь доверенным пользователем'
        )
    return True
