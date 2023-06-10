from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from src.database import Base
from src.json_responses import (
    OkJSONResponse, CreateJSONResponse, NotFoundJSONResponse,
    BadRequestJSONResponse
)
from src.crud import BaseObjectCRUD


async def get_object(
        model: Base,
        scheme: BaseModel,
) -> JSONResponse:
    if model:
        return JSONResponse(
            content=scheme.dict(),
            status_code=HTTP_200_OK,
        )
    else:
        return NotFoundJSONResponse


async def create_object(
        obj: BaseObjectCRUD,
        session: AsyncSession
) -> JSONResponse:
    if await obj.read(session):
        return OkJSONResponse

    else:
        await obj.create(session)
        await session.commit()
        return CreateJSONResponse


async def update_object(
        original_obj: BaseObjectCRUD,
        new_obj: BaseObjectCRUD,
        data_for_update: dict,
        session: AsyncSession
) -> JSONResponse:
    if await original_obj.read(session):

        if await new_obj.read(session) is None:

            if await original_obj.read(session) != await new_obj.read(session):
                await original_obj.update(data_for_update, session)
                await session.commit()
                return OkJSONResponse

            else:
                await original_obj.create(session)
                await session.commit()
                return CreateJSONResponse
        else:
            return BadRequestJSONResponse
    else:
        return NotFoundJSONResponse


async def delete_object(
        obj: BaseObjectCRUD,
        session: AsyncSession
) -> JSONResponse:
    if await obj.read(session):
        await obj.delete(session)
        await session.commit()
        return OkJSONResponse

    else:
        return NotFoundJSONResponse


async def execute_first_object(session, query):
    result = await session.execute(query)
    return result.scalars().first()
