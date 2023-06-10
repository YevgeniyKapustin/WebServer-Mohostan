from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.database import get_async_session
from src.commands.models import Command
from src.commands.schemas import CommandScheme, CommandCreateScheme
from src.commands.services import CommandCRUD
from src.default_responses import (
    get_get_response, get_update_response, get_create_response,
    get_delete_response
)
from src.services import (
    update_object, delete_object, create_object, get_object
)

router = APIRouter(
    prefix='/api/v1/commands',
    tags=['Команды'],
)


@router.get(
    '/{id}',
    name='Возвращает информацию о команде',
    responses=get_get_response(CommandScheme)
)
@cache(expire=60)
async def get_command(
        id_: int,

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:

    model: Command = await CommandCRUD(id_).read(session)
    scheme = CommandScheme(
        id=model.id,
        type_id=model.type_id,
        request=model.request,
        response=model.response
    ) if hasattr(model, 'id') else ...

    return await get_object(model, scheme)


@router.post(
    '/',
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
    '/{id}',
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
    '/',
    name='Удаляет команду',
    responses=get_delete_response()
)
async def delete_type(
        command_id: int,

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:

    obj = CommandCRUD(command_id)
    return await delete_object(obj, session)
