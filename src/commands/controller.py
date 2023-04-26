from fastapi import APIRouter

from commands.models import Type
from database import session

router = APIRouter(
    prefix='/api/v1',
    tags=['База'],
)


@router.get("/")
async def get_databases():
    return session.query(Type).first()
