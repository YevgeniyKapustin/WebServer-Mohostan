from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin

from src.users.services.database import get_user_db, User
from src.config import SECRET_KEY


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
