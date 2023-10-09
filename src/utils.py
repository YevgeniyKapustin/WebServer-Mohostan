from typing import Type

from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from src.constants import (
    NotFoundJSONResponse, OkJSONResponse, CreateJSONResponse,
    BadRequestJSONResponse
)
from src.database import Base
from src.service import BaseCRUD


async def get_single_object(
        model: Base,
        scheme: BaseModel,
) -> JSONResponse:
    """Возвращает один объект из модели по схеме."""
    if model:
        return JSONResponse(
            content=scheme.dict(),
            status_code=HTTP_200_OK,
        )
    else:
        return NotFoundJSONResponse


async def get_objects(
        model: BaseCRUD,
        scheme: Type[BaseModel],
        session: AsyncSession

) -> JSONResponse:
    """Возвращает список объектов из crud объекта по схеме."""
    if obj_list := await model.get(session):

        response: list[dict] = [
            {
                attr: getattr(obj, attr)
                for attr in scheme.schema().get('properties')
            }
            for obj in obj_list
        ]
        return JSONResponse(
            content=response,
            status_code=HTTP_200_OK,
        )

    else:
        return NotFoundJSONResponse


async def create_object(
        obj: BaseCRUD,
        session: AsyncSession
) -> JSONResponse:
    """Создает объект в базе из crud объекта."""
    if await obj.get_same(session):
        return OkJSONResponse

    else:
        await obj.create(session)
        await session.commit()
        return CreateJSONResponse


async def update_object(
        original_obj: BaseCRUD,
        new_obj: BaseCRUD,
        data_for_update: dict,
        session: AsyncSession
) -> JSONResponse:
    """Обновляет original_obj с помощью data_for_update."""
    original_obj_orm = await original_obj.get(session)
    new_obj_orm = await new_obj.get(session)

    if original_obj_orm:

        if not new_obj_orm:

            if original_obj_orm == new_obj_orm:
                await original_obj.create(session)
                await session.commit()
                return CreateJSONResponse

            else:
                await original_obj.update(data_for_update, session)
                await session.commit()
                return OkJSONResponse
        else:
            return BadRequestJSONResponse
    else:
        return NotFoundJSONResponse


async def delete_object(
        obj: BaseCRUD,
        session: AsyncSession
) -> JSONResponse:
    """Удаляет объект crud из базы."""
    if await obj.get(session):
        await obj.delete(session)
        await session.commit()
        return OkJSONResponse

    else:
        return NotFoundJSONResponse


async def execute_first_object(
        session: AsyncSession,
        query: Select
) -> Base:
    """Достает один объект из сессии."""
    result = await session.execute(query)
    return result.scalars().first()


async def execute_all_objects(
        session: AsyncSession,
        query: Select
) -> list:
    """Достает список объектов из сессии."""
    result = await session.execute(query)
    return list(result.scalars().all())
