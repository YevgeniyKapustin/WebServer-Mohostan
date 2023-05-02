from fastapi import APIRouter
from fastapi_cache.decorator import cache
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_200_OK
)

from src.commands_types.models import Type as TypeModel
from src.commands_types.schemas import TypeScheme
from src.commands_types.services import get_type_by_name, create_type_by_name
from src.database import session
from src.responses.json import OkJSONResponse, NotFoundJSONResponse
from src.responses.schemas import CreateScheme, NotFoundScheme, OkScheme

router = APIRouter(
    prefix='/api/v1/types',
    tags=['Типы команд'],
)


@router.get("/")
@cache(expire=60)
async def get_all_types():
    query = session.query(TypeModel)

    return {
        'types': query.all(),
        'message': 'success'
    }


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
async def get_type(name: str):
    type_by_name = await get_type_by_name(name)

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
async def create_type(command_type: TypeScheme) -> CreateScheme():

    if await get_type_by_name(command_type.name):
        return OkJSONResponse

    else:
        await create_type_by_name(command_type.name)
        return CreateScheme


@router.put("/")
async def update_type(command_type: TypeScheme):
    session.add(TypeModel(type=command_type.name))
    session.commit()

    stmt = session.query(TypeModel).where(TypeModel.type == command_type.name)

    return {
        'type': stmt.first(),
        'message': 'success'
    }


@router.delete("/")
async def delete_type(command_type: TypeScheme):
    stmt = session.query(TypeModel).where(TypeModel.name == command_type.name)
    if stmt.first():
        session.delete(stmt.first())
        session.commit()

        return {
            'message': 'success'
        }

    else:

        return JSONResponse(
            content={"message": "Resource Not Found"},
            status_code=HTTP_404_NOT_FOUND
        )
