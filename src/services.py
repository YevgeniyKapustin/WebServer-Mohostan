from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from src.database import Base
from src.json_responses import (
    OkJSONResponse, CreateJSONResponse, NotFoundJSONResponse,
    BadRequestJSONResponse
)
from src.crud import BaseObjectCRUD


async def get_object(model: Base, scheme: BaseModel) -> JSONResponse:
    if model:
        return JSONResponse(
            content=scheme.dict(),
            status_code=HTTP_200_OK,
        )
    else:
        return NotFoundJSONResponse


async def create_object(obj: BaseObjectCRUD) -> JSONResponse:
    if await obj.read():
        return OkJSONResponse

    else:
        await obj.create()
        return CreateJSONResponse


async def update_object(
        original_obj: BaseObjectCRUD,
        new_obj: BaseObjectCRUD,
        data_for_update: dict

) -> JSONResponse:
    if await original_obj.read():

        if await new_obj.read() is None:

            if await original_obj.read() != await new_obj.read():
                await original_obj.update(data_for_update)
                return OkJSONResponse

            else:
                await original_obj.create()
                return CreateJSONResponse
        else:
            return BadRequestJSONResponse
    else:
        return NotFoundJSONResponse


async def delete_object(obj: BaseObjectCRUD) -> JSONResponse:
    if await obj.read():
        await obj.delete()
        return OkJSONResponse

    else:
        return NotFoundJSONResponse


async def execute_first_object(session, query):
    result = await session.execute(query)
    return result.scalars().first()
