from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

from database import Base
from responses import (
    OkJSONResponse, CreateJSONResponse, NotFoundJSONResponse,
    BadRequestJSONResponse
)
from crud import BaseObjectCRUD


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
        data_for_update: tuple

) -> JSONResponse:
    if await original_obj.read():

        if not await new_obj.read():

            if await original_obj.read() != await new_obj.read():
                await original_obj.update(data_for_update)
                return OkJSONResponse

            else:
                await original_obj.create()
                return CreateJSONResponse
        else:
            return NotFoundJSONResponse
    else:
        return BadRequestJSONResponse


async def delete_object(obj: BaseObjectCRUD) -> JSONResponse:
    if await obj.read():
        await obj.delete()
        return OkJSONResponse

    else:
        return NotFoundJSONResponse
