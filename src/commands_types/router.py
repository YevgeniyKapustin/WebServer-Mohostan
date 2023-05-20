from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from starlette.responses import JSONResponse

from default_responses import (
    get_get_response, get_update_response, get_create_response,
    get_delete_response
)
from src.services import (
    update_object, delete_object, create_object, get_object
)
from src.commands_types.schemas import TypeScheme, TypeCreateScheme
from src.commands_types.services import TypeCRUD
from src.users.models import User
from src.users.services import get_current_user_by_token
from src.utils import trust_check

router = APIRouter(
    prefix='/api/v1/types',
    tags=['Типы команд'],
)


@router.get(
    "/{id}",
    name="Возвращает информацию о типе команды",
    responses=get_get_response(TypeScheme)
)
@cache(expire=60)
async def get_type(
        id: int,
        current_user: User = Depends(get_current_user_by_token)

) -> JSONResponse:
    trust_check(current_user)

    model = await TypeCRUD(id).read()
    scheme = TypeScheme(
        id=model.id,
        name=model.name
    ) if hasattr(model, 'id') else ...

    return await get_object(model, scheme)


@router.post(
    '/',
    name="Создает тип команды",
    description='''
    Создает тип для команд, вы сможете самостоятельно обрабатывать команды 
    этого типа уже на своем клиенте, тут они только создаются и хранятся.
    ''',
    responses=get_create_response()
)
async def create_type(
        command_type: TypeCreateScheme,
        current_user: User = Depends(get_current_user_by_token),

) -> JSONResponse:
    trust_check(current_user)

    obj = TypeCRUD(name=command_type.name)
    return await create_object(obj)


@router.put(
    "/{id}",
    name="Изменяет имя типа команды",
    responses=get_update_response()
)
async def update_type(
        id: int,
        new_type: TypeCreateScheme,
        current_user: User = Depends(get_current_user_by_token),

) -> JSONResponse:
    trust_check(current_user)

    original_obj = TypeCRUD(id_=id)
    new_obj = TypeCRUD(name=new_type.name)
    data_for_update = (new_type.name,)

    return await update_object(original_obj, new_obj, data_for_update)


@router.delete(
    "/",
    name="Удаляет тип команды",
    responses=get_delete_response()
)
async def delete_type(
        id: int,
        current_user: User = Depends(get_current_user_by_token),

) -> JSONResponse:
    trust_check(current_user)

    obj = TypeCRUD(id)
    return await delete_object(obj)
