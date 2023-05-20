from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)

from src.services import (
    update_object, delete_object, create_object, get_object
)
from src.commands.schemas import TypeScheme
from src.commands.services import TypeCRUD
from src.schemas import (
    CreateScheme, NotFoundScheme, OkScheme, BadRequestScheme
)
from src.users.models import User
from src.users.services import get_current_user_by_token
from utils import trust_check

router = APIRouter(
    prefix='/api/v1/types',
    tags=['Команды / Типы'],
)


@router.get(
    "/{name}",
    name="Возвращает информацию о типе команды",
    status_code=HTTP_200_OK,
    response_model=TypeScheme,
    responses={
        HTTP_200_OK: {
            'model': TypeScheme,
            'description': 'Тип получен',
        },
        HTTP_404_NOT_FOUND: {
            'model': NotFoundScheme,
            'description': 'Типа не существует',
        }
    }
)
@cache(expire=60)
async def get_type(
        name: str,
        current_user: User = Depends(get_current_user_by_token)

) -> JSONResponse:
    trust_check(current_user)

    model = await TypeCRUD(name).read()
    scheme = TypeScheme(
        id=model.id,
        name=model.name
    ) if hasattr(model, 'id') else ...

    return await get_object(model, scheme)


@router.post(
    '/',
    name="Создает тип команды",
    description='''
    Создает тип для команд, вы сможете самостоятельно обрабатывать команды 
    этого типа уже на своем клиенте, тут они только создаются и хранятся.
    ''',
    status_code=HTTP_201_CREATED,
    response_model=CreateScheme,
    responses={
        HTTP_200_OK: {
            'model': OkScheme,
            'description': 'Тип уже существует',
        },
        HTTP_201_CREATED: {
            'model': CreateScheme,
            'description': 'Тип создан',
        }
    }
)
async def create_type(
        command_type: TypeScheme,
        current_user: User = Depends(get_current_user_by_token),

) -> JSONResponse:
    trust_check(current_user)

    obj = TypeCRUD(command_type.name)
    return await create_object(obj)


@router.put(
    "/{name}",
    name="Изменяет имя типа команды",
    status_code=HTTP_200_OK,
    response_model=TypeScheme,
    responses={
        HTTP_200_OK: {
            'model': OkScheme,
            'description': 'Объект изменен',
        },
        HTTP_201_CREATED: {
            'model': CreateScheme,
            'description': 'Объект создан',
        },
        HTTP_400_BAD_REQUEST: {
            'model': BadRequestScheme,
            'description': 'Конечный объект уже существует'
        },
        HTTP_404_NOT_FOUND: {
            'model': NotFoundScheme,
            'description': 'Объект не существует',
        },
    }
)
async def update_type(
        name: str,
        new_type: TypeScheme,
        current_user: User = Depends(get_current_user_by_token),

) -> JSONResponse:
    trust_check(current_user)

    original_obj = TypeCRUD(name)
    new_obj = TypeCRUD(new_type.name)
    data_for_update = (new_type.name,)

    return await update_object(original_obj, new_obj, data_for_update)


@router.delete(
    "/",
    name="Удаляет тип команды",
    status_code=HTTP_200_OK,
    response_model=TypeScheme,
    responses={
        HTTP_200_OK: {
            'model': OkScheme,
            'description': 'Объект удален',
        },
        HTTP_404_NOT_FOUND: {
            'model': NotFoundScheme,
            'description': 'Объект не существует',
        },
    }
)
async def delete_type(
        command_type: TypeScheme,
        current_user: User = Depends(get_current_user_by_token),

) -> JSONResponse:
    trust_check(current_user)

    obj = TypeCRUD(command_type.name)
    return await delete_object(obj)
