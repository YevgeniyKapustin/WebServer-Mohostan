import os
from datetime import datetime

import aiofiles
from fastapi import HTTPException, UploadFile
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.utils import execute_all_objects
from src.service import BaseCRUD
from src.videos.models import Video


class VideoCRUD(BaseCRUD):
    """Класс описывающий поведение видео."""
    __id: int | None
    __title: str | None
    __file: UploadFile | None
    __path: str | None

    def __init__(
            self,
            id_: int = None,
            title: str = None,
            file: UploadFile = None,
            path: str = None
    ):
        self.__id: int = id_
        self.__title: str = title
        self.__file: UploadFile = file
        self.__path: str = path

    async def get(self, session: AsyncSession) -> list:
        """Чтение видео из базы данных."""
        if self.__id or self.__title or self.__path:
            query = (
                select(Video).
                where(
                    or_(
                        Video.title == self.__title,
                        Video.id == self.__id,
                        Video.path == self.__path,
                    )
                )
            )
        else:
            query = (select(Video))
        return await execute_all_objects(session, query)

    async def create(self, session) -> bool:
        """Добавление видео в сессию и в static."""
        self.__path = f'{self.__title}{int(datetime.now().timestamp())}.mp4'
        if self.__file.content_type == 'video/mp4':
            file_path = f'{settings.STATIC_DIR}/{self.__path}'
            async with aiofiles.open(file_path, "wb") as buffer:
                await buffer.write(await self.__file.read())
            session.add(Video(title=self.__title, path=self.__path))
            return True
        else:
            raise HTTPException(status_code=418, detail='Файл должен быть mp4')

    async def update(self, new_obj: dict, session: AsyncSession) -> bool:
        """Обновление видео в сессии."""
        self.__title = new_obj.get('title')

        objs: list = await self.get(session)
        first_obj = objs[0]

        if first_obj:
            first_obj.title = self.__title
            session.add(first_obj)
            return True

        return False

    async def delete(self, session: AsyncSession) -> bool:
        """Удаление видео из сессии."""
        objs: list = await self.get(session)
        first_obj = objs[0]
        await session.delete(first_obj)
        os.remove(f'{settings.STATIC_DIR}/{first_obj.path}')
        return True
