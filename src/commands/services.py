from loguru import logger
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
            logger.info(f'Создание команды "{self.__request}"...')
            session.add(
                Command(
                    type=self.__type,
                    request=self.__request,
                    response=self.__response,
                )
            )
            logger.info(f'Команда "{self.__request}" создана.')
            return True
        logger.debug(
            f'''Для создания команды не хватает некоторых данных:
            type: {self.__type}
            request: {self.__request}
            response: {self.__response}
            ''')
        return False

    async def read(self, session: AsyncSession) -> list | None:
        """Чтение объекта из базы данных."""
        query = None
        if self.__type and self.__request:
            query = (
                select(Command).
                where(
                    Command.request == self.__request,
                    Command.type == self.__type,
                )
            )

        elif self.__type:
            query = (
                select(Command).
                where(
                    Command.type == self.__type,
                )
            )

        elif self.__request:
            query = (
                select(Command).
                where(
                    Command.request == self.__request,
                )
            )

        elif self.__id:
            query = (
                select(Command).
                where(
                    Command.id == self.__id,
                )
            )

        return await self.__execute_commands(session, query)

    async def update(self, new_obj: dict, session: AsyncSession) -> bool:
        """Обновление объекта в базы данных."""
        self.__request = new_obj.get('request')
        self.__response = new_obj.get('response')
        self.__type = new_obj.get('type')

        obj = (await self.read(session))
        if obj:
            obj.type = self.__type,
            obj.request = self.__request,
            obj.response = self.__response,

            session.add(obj)
            return True
        return False

    async def delete(self, session: AsyncSession) -> bool:
        """Удаление объекта из базы данных."""
        commands = await self.read(session)
        [await session.delete(obj) for obj in await self.read(session)]
        logger.info(f'Удалены команды {commands}.')
        return True

    @staticmethod
    async def __execute_commands(session, query) -> list | None:
        if query:
            commands: list = await execute_all_objects(session, query)
            logger.info(f'Найдены команды {commands}.')
            return commands
        logger.info(f'Не удалось найти подходящую команду.')
        return None
