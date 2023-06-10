from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import execute_first_object
from src.crud import BaseObjectCRUD
from src.commands.models import Command


class CommandCRUD(BaseObjectCRUD):
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
            response: str = None
    ):
        self.__id: int = id_
        self.__type: str = type_
        self.__request: str = request
        self.__response: str = response

    async def create(self, session) -> bool:
        """Создание объекта в базе данных."""
        session.add(
            Command(
                type=self.__type,
                request=self.__request,
                response=self.__response,
            )
        )
        return True

    async def read(self, session: AsyncSession) -> Command | None:
        """Чтение объекта из базы данных."""
        if self.__id:
            query = (
                select(Command).
                where(Command.id == self.__id)
            )
            return await execute_first_object(session, query)

        elif self.__request and self.__type and self.__response:
            query = (
                select(Command).
                where(
                    Command.request == self.__request,
                    Command.type == self.__type,
                    Command.response == self.__response,
                )
            )
            return await execute_first_object(session, query)

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
