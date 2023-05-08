from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from json_responses import CreateJSONResponse
from src.schemas import CreateScheme
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.users import schemas
from src.users.services import authenticate_user, create_user
from src.users.utils import create_access_token

router = APIRouter(
    prefix='/api/v1/auth',
    tags=['Аутентификация'],
)


@router.post(
    "/login",
    name="Получить токен для пользователя",
    status_code=HTTP_200_OK,
    response_model=schemas.Token
)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> schemas.Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не верный логин или пароль',
        )

    access_token = create_access_token(
        data={
            'sub': user.email
        },
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return schemas.Token(
        access_token=access_token,
        token_type='bearer'
    )


@router.post(
    "/registration",
    name="Регистрация",
    status_code=HTTP_201_CREATED,
    response_model=CreateScheme
)
async def register_user(user: schemas.UserCreate) -> CreateScheme:
    await create_user(user)
    return CreateJSONResponse
