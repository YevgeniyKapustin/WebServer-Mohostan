from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND

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
from src.types.services import TypeCRUD
from src.users.models import User
from src.users.services import get_current_user_by_token
from src.utils import trust_check

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
        id: int,

        current_user: User = Depends(get_current_user_by_token),
        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    trust_check(current_user)

    model: Command = await CommandCRUD(session, id).read()
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

        current_user: User = Depends(get_current_user_by_token),
        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    trust_check(current_user)

    if not (command_type := await TypeCRUD(session, command.type_id).read()):
        raise HTTPException(HTTP_404_NOT_FOUND, detail='Тип не найден')

    obj = CommandCRUD(
        session,
        type_=command_type,
        request=command.request,
        response=command.response,
    )
    return await create_object(obj)


@router.put(
    '/{id}',
    name='Изменяет команду',
    responses=get_update_response()
)
async def update_command(
        id: int,
        new_command: CommandCreateScheme,

        current_user: User = Depends(get_current_user_by_token),
        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    trust_check(current_user)

    original_obj = CommandCRUD(session, id=id)
    new_obj = CommandCRUD(
        session,
        type_=await TypeCRUD(session, id=new_command.type_id).read(),
        request=new_command.request,
        response=new_command.response,
    )
    data_for_update = (new_command.dict())

    return await update_object(original_obj, new_obj, data_for_update)


@router.delete(
    '/',
    name='Удаляет команду',
    responses=get_delete_response()
)
async def delete_type(
        command_id: int,

        current_user: User = Depends(get_current_user_by_token),
        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    trust_check(current_user)

    obj = CommandCRUD(session, command_id)
    return await delete_object(obj)
