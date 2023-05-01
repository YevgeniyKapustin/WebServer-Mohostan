from fastapi import APIRouter
from fastapi_cache.decorator import cache
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_200_OK
)

from src.commands_types.models import Type as TypeModel
from src.commands_types.schemas import Type as TypeScheme
from src.commands_types.services import get_type_by_name, create_type_by_name
from src.database import session
from src.schemas.response import OkResponse, CreateResponse

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


@router.get("/{name}")
@cache(expire=60)
async def get_type(name: str):
    query = session.query(TypeModel).where(TypeModel.name == name)

    if query.first():

        return {
            'type': query.first(),
            'message': 'success'
        }

    else:

        return JSONResponse(
            content={"message": "Resource Not Found"},
            status_code=HTTP_404_NOT_FOUND
        )


@router.post(
    '/',
    name="Создать тип команды",
    description='''
    Создает тип для команд, вы сможете самостоятельно обрабатывать команды 
    этого типа уже на своем клиенте, тут они только создаются и хранятся.
    ''',
    response_model=CreateResponse,
    status_code=HTTP_201_CREATED,
    responses={
        HTTP_200_OK: {
            'model': OkResponse,
            'description': 'Объект уже существует',
        },
        HTTP_201_CREATED: {
            'model': CreateResponse,
            'description': 'Объект создан',
        },
    }
)
async def create_type(command_type: TypeScheme) -> CreateResponse():

    if await get_type_by_name(command_type.name):
        return JSONResponse(
            content=OkResponse().dict(),
            status_code=HTTP_200_OK,
        )

    else:
        await create_type_by_name(command_type.name)
        return JSONResponse(
            content=CreateResponse().dict(),
            status_code=HTTP_201_CREATED,
        )


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
