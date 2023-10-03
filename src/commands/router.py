from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.constants import (
    get_get_response, get_create_response, get_update_response,
    get_delete_response
)
from src.database import get_async_session
from src.commands.schemas import CommandScheme, CommandCreateScheme
from src.commands.services import CommandCRUD
from src.utils import (
    update_object, delete_object, create_object, get_objects
)

router = APIRouter(
    prefix='/api/v1/',
    tags=['Команды'],
)


@router.get(
    'commands',
    name='Возвращает информацию о команде',
    description='''
    Предоставляет список команд по запросу.
    ''',
    responses=get_get_response(CommandScheme)
)
@cache(expire=60)
async def get_command(
        command_type: Annotated[
            str | None,
            Query(
                title='Тип команды',
            )
        ] = None,
        request_: Annotated[
            str | None,
            Query(
                title='Текст команды',
                alias='request',
            )
        ] = None,
        is_inline: Annotated[
            bool,
            Query(
                title='Поиск команды внутри запроса',
            )
        ] = False,

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    crud: CommandCRUD = CommandCRUD(
        type_=command_type, request=request_, is_inline=is_inline
    )

    return await get_objects(crud, CommandScheme, session)


@router.post(
    'commands/',
    name='Создает команду',
    responses=get_create_response()
)
async def create_command(
        command: CommandCreateScheme,

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    obj = CommandCRUD(
        type_=command.type,
        request=command.request,
        response=command.response,
    )
    return await create_object(obj, session)


@router.put(
    'commands/{id}',
    name='Изменяет команду',
    responses=get_update_response()
)
async def update_command(
        id_: int,
        new_command: CommandCreateScheme,

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    original_obj = CommandCRUD(id_=id_)
    new_obj = CommandCRUD(
        type_=new_command.type,
        request=new_command.request,
        response=new_command.response,
    )
    data_for_update = (new_command.dict())

    return await update_object(original_obj, new_obj, data_for_update, session)


@router.delete(
    'commands/',
    name='Удаляет команду',
    responses=get_delete_response()
)
async def delete_type(
        command_id: int,

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    obj = CommandCRUD(command_id)
    return await delete_object(obj, session)
