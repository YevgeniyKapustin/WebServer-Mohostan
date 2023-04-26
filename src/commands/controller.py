from fastapi import APIRouter
from fastapi_cache.decorator import cache

from commands.models import Type
from database import session

router = APIRouter(
    prefix='/api/v1',
    tags=['База'],
)


@router.get("/")
@cache(expire=200)
async def get_databases():
    return session.query(Type).first()
