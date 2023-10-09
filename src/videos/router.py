from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, Query, Path, Body, File
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, FileResponse

from src.config import settings
from src.constants import (
    get_get_response, get_update_response, get_delete_response,
    get_video_create_response
)
from src.database import get_async_session
from src.utils import (
    update_object, delete_object, create_object, get_objects
)
from src.videos.schemas import VideoScheme, VideoCreateScheme
from src.videos.services import VideoCRUD

router = APIRouter(
    prefix='/api/v1',
    tags=['Видео'],
)


@router.delete(
    '/videos/{id}',
    name='Удалить видео',
    description='''
    Удаляет видео и данные о нем.
    ''',
    responses=get_delete_response()
)
async def delete_video(
        id_: Annotated[
            int,
            Path(
                title='ID видео',
                description='Получить ID можно по запросу информации о видео.',
                alias='id',
                ge=1
            )
        ],

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    obj: VideoCRUD = VideoCRUD(id_)
    return await delete_object(obj, session)


@router.get(
    '/videos',
    name='Получить информацию о видео',
    description='''
    Предоставляет информацию об искомом видео.<br>
    Обычно вам нужно использовать только одно поле поиска.<br>
    Если не использовать поля поиска будут возвращены все видео.<br>
    Значение кэшируется на `минуту`.
    ''',
    responses=get_get_response(VideoScheme)
)
@cache(expire=60)
async def get_video(
        id_: Annotated[
            int | None,
            Query(
                title='ID видео',
                description='Для поиска по ID используйте это поле',
                alias='id',
                ge=1
            )
        ] = None,
        title: Annotated[
            str | None,
            Query(
                title='Название видео',
                description='Для поиска по названию используйте это поле',
                alias='name',
                min_length=3,
                max_length=50
            )
        ] = None,

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    obj: VideoCRUD = VideoCRUD(id_=id_, title=title)
    return await get_objects(obj, VideoScheme, session)


@router.get(
    '/videos/download/{path:path}',
    name='Скачать видео',
    description='''
    Отправляет первое видео соответствующее запросу.<br>
    Внимание! Значение кэшируется на `10 минут`.
    ''',
    response_class=FileResponse
)
@cache(expire=600)
async def download_video(
        path: str,

        session: AsyncSession = Depends(get_async_session),

) -> FileResponse:
    videos: list = await VideoCRUD(path=path).get(session)
    return FileResponse(f'{settings.STATIC_DIR}/{videos[0].path}')


@router.post(
    '/videos',
    name='Загрузить видео',
    description='''
    Загружает видео на сервер.
    ''',
    responses=get_video_create_response()
)
async def create_video(
        title: Annotated[
            str,
            Body(
                title='Название видео',
                description='Название поможет вам найти свое видео.',
                alias='name',
                min_length=3,
                max_length=50
            )
        ],
        file: Annotated[
            UploadFile,
            File(
                title='mp4 видео',
            )
        ],

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    obj: VideoCRUD = VideoCRUD(title=title, file=file)
    return await create_object(obj, session)


@router.put(
    '/videos/{id}',
    name='Переименовать видео',
    description='''
    Меняет название видео.<br>
    Эта операция не меняет путь!
    ''',
    responses=get_update_response()
)
async def update_command(
        id_: Annotated[
            int | None,
            Path(
                title='ID видео',
                alias='id',
                ge=1
            )
        ],
        new_video: VideoCreateScheme,

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    original_obj = VideoCRUD(id_=id_)
    new_obj = VideoCRUD(title=new_video.title)
    data_for_update = new_video.dict()

    return await update_object(original_obj, new_obj, data_for_update, session)
