from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import execute_all_objects
from src.service import BaseCRUD
from src.commands.models import Command


class CommandCRUD(BaseCRUD):
    """Класс описывающий поведение команд."""
    __id: int | None
    __type: str | None
    __request: str | None
    __response: str | None

    def __init__(
            self,
            id_: int = None,
            type_: str = None,
            request: str = None,
            response: str = None,
    ):
        self.__id: int = id_
        self.__type: str = type_
        self.__request: str = request
        self.__response: str = response

    async def create(self, session) -> bool:
        """Создание объекта в базе данных."""
        if self.__type and self.__request and self.__response:
            session.add(
                Command(
                    type=self.__type,
                    request=self.__request,
                    response=self.__response,
                )
            )
            return True
        return False

    async def read(self, session: AsyncSession) -> list[Command] | None:
        """Чтение объекта из базы данных."""
        if self.__type and self.__request:
            query = (
                select(Command).
                where(
                    Command.request == self.__request,
                    Command.type == self.__type,
                )
            )
            return await execute_all_objects(session, query)

        elif self.__type:
            query = (
                select(Command).
                where(
                    Command.type == self.__type,
                )
            )
            return await execute_all_objects(session, query)

        elif self.__request:
            query = (
                select(Command).
                where(
                    Command.request == self.__request,
                )
            )
            return await execute_all_objects(session, query)

        return None

    async def update(self, new_obj: dict, session: AsyncSession) -> bool:
        """Обновление объекта в базы данных."""
        self.__request = new_obj.get('request')
        self.__response = new_obj.get('response')
        self.__type = new_obj.get('type')

        obj = await self.read(session)
        obj.type = self.__type,
        obj.request = self.__request,
        obj.response = self.__response,

        session.add(obj)
        return True

    async def delete(self, session: AsyncSession) -> bool:
        """Удаление объекта из базы данных."""
        await session.delete(await self.read(session))
        return True
