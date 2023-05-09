from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_200_OK
)

from src.commands_types.schemas import TypeScheme
from src.commands_types.services import TypeCRUD
from src.json_responses import (
    OkJSONResponse, NotFoundJSONResponse, NoContentJSONResponse,
    CreateJSONResponse
)
from src.schemas import CreateScheme, NotFoundScheme, OkScheme
from src.users.models import User
from src.users.services import get_current_user_by_token

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
async def get_type(name: str) -> JSONResponse:
    type_by_name = await TypeCRUD(name).read()

    if type_by_name:
        obj = TypeScheme(
            id=type_by_name.id,
            name=type_by_name.name
        )
        return JSONResponse(
            content=obj.dict(),
            status_code=HTTP_200_OK,
        )

    else:
        return NotFoundJSONResponse


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
    if await TypeCRUD(command_type.name).read():
        return OkJSONResponse

    else:
        await TypeCRUD(command_type.name).create()
        return CreateJSONResponse


@router.put(
    "/{name}",
    name="Изменяет имя типа команды",
    status_code=HTTP_200_OK,
    response_model=TypeScheme,
    responses={
        HTTP_200_OK: {
            'model': OkScheme,
            'description': 'Тип изменен',
        },
        HTTP_201_CREATED: {
            'model': CreateScheme,
            'description': 'Тип создан',
        },
    }
)
async def update_type(name: str, new_type: TypeScheme) -> JSONResponse:
    original_obj = TypeCRUD(name)
    new_obj = TypeCRUD(new_type.name)

    if await original_obj.read() and not await new_obj.read():

        if await original_obj.read() != await new_obj.read():
            await original_obj.update(new_type.name)
            return OkJSONResponse

        else:
            await original_obj.create()
            return CreateJSONResponse

    else:
        return NoContentJSONResponse


@router.delete(
    "/",
    name="Удаляет тип команды",
    status_code=HTTP_200_OK,
    response_model=TypeScheme,
    responses={
        HTTP_200_OK: {
            'model': OkScheme,
            'description': 'Тип удален',
        },
        HTTP_404_NOT_FOUND: {
            'model': NotFoundScheme,
            'description': 'Типа не существует',
        },
    }
)
async def delete_type(command_type: TypeScheme) -> JSONResponse:
    obj = TypeCRUD(command_type.name)

    if await obj.read():
        await obj.delete()
        return OkJSONResponse

    else:
        return NotFoundJSONResponse
