from fastapi import APIRouter
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND

from commands_types.models import Type
from database import session

router = APIRouter(
    prefix='/api/v1/types',
    tags=['Типы команд'],
)


class TypeBody(BaseModel):
    name: str


@router.get("/")
@cache(expire=60)
async def get_all_types():
    query = session.query(Type)

    return {
        'types': query.all(),
        'message': 'success'
    }


@router.get("/{name}")
@cache(expire=60)
async def get_type(name: str):
    query = session.query(Type).where(Type.type == name)

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


@router.post("/")
async def add_type(command_type: TypeBody):
    session.add(Type(type=command_type.name))
    session.commit()

    stmt = session.query(Type).where(Type.type == command_type.name)

    return {
        'type': stmt.first(),
        'message': 'success'
    }


@router.put("/")
async def update_type(command_type: TypeBody):
    session.add(Type(type=command_type.name))
    session.commit()

    stmt = session.query(Type).where(Type.type == command_type.name)

    return {
        'type': stmt.first(),
        'message': 'success'
    }


@router.delete("/")
async def delete_type(command_type: TypeBody):
    stmt = session.query(Type).where(Type.type == command_type.name)

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
