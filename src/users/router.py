from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.database import get_async_session
from src.json_responses import CreateJSONResponse
from src.schemas import CreateScheme, OkScheme
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
    response_model=schemas.Token,
    responses={
        HTTP_200_OK: {
            'model': OkScheme,
            'description': 'Токен получен',
        }
    }
)
async def get_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_async_session),

) -> schemas.Token:
    user = await authenticate_user(
        session, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не верный логин или пароль',
        )

    access_token = await create_access_token(
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
    response_model=CreateScheme,
    responses={
        HTTP_200_OK: {
            'model': OkScheme,
            'description': 'Пользователь уже существует',
        },
        HTTP_201_CREATED: {
            'model': CreateScheme,
            'description': 'Пользователь создан',
        },
    }
)
async def register_user(
        user: schemas.UserCreate,

        session: AsyncSession = Depends(get_async_session)

) -> CreateScheme:
    await create_user(session, user)
    return CreateJSONResponse
