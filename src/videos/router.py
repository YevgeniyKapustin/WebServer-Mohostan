from fastapi import APIRouter, Depends, UploadFile
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, FileResponse

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
from src.videos.schemas import VideoScheme, VideoCreateScheme
from src.videos.services import VideoCRUD

router = APIRouter(
    prefix='/api/v1/videos',
    tags=['Видео'],
)


@router.get(
    '/',
    name='Получить видео',
    description='''
    Предоставляет видео.
    ''',
    responses=get_get_response(VideoScheme)
)
@cache(expire=60)
async def get_video(
        id_: int | None = None,
        title: str | None = None,

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    obj: VideoCRUD = VideoCRUD(
        id_=id_,
        title=title,
    )
    return await get_objects(obj, VideoScheme, session)


@router.get(
    '/download',
    name='Скачать видео',
    description='''
    Отправляет первое видео соответствующее запросу.
    ''',
    responses=get_get_response(VideoScheme)
)
@cache(expire=60)
async def download_video(
        id_: int | None = None,
        title: str | None = None,
        path: str | None = None,

        session: AsyncSession = Depends(get_async_session),

) -> FileResponse:
    obj: VideoCRUD = VideoCRUD(
        id_=id_,
        title=title,
        path=path
    )
    videos = await obj.read(session)
    return FileResponse(videos[0].path)


@router.post(
    '/',
    name='Загрузить видео',
    responses=get_create_response()
)
async def create_video(
        title: str,
        file: UploadFile,

        session: AsyncSession = Depends(get_async_session),
) -> JSONResponse:
    obj: VideoCRUD = VideoCRUD(
        title=title,
        file=file,
    )
    return await create_object(obj, session)


@router.put(
    '/{id_}',
    name='Изменяет команду',
    responses=get_update_response()
)
async def update_command(
        id_: int,
        new_video: VideoCreateScheme,

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    original_obj = VideoCRUD(id_=id_)
    new_obj = VideoCRUD(
        title=new_video.title,
    )
    data_for_update = (new_video.dict())

    return await update_object(original_obj, new_obj, data_for_update, session)


@router.delete(
    '/',
    name='Удаляет видео',
    responses=get_delete_response()
)
async def delete_type(
        id_: int,

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    obj = VideoCRUD(id_)
    return await delete_object(obj, session)
