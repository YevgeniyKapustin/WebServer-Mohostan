from fastapi import APIRouter
from fastapi_cache.decorator import cache
from pydantic import BaseModel

from commands.models import Type
from database import session

router = APIRouter(
    prefix='/api/v1',
    tags=['База'],
)


@router.get("/type/{name}")
@cache(expire=60)
async def get_types(name: str):
    result = session.query(Type).where(Type.type == name)
    return {'type': result.all()}


@router.get("/type")
@cache(expire=60)
async def get_all_types():
    return {'type': session.query(Type).all()}


class TypeBody(BaseModel):
    name: str


@router.post("/type")
async def add_command(command_type: TypeBody):
    name = command_type.name

    session.add(Type(name=name))
    session.commit()

    return {'type': session.query(Type).where(name == name)}
