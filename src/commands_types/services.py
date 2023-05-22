from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import execute_first_object
from src.crud import BaseObjectCRUD
from src.commands_types.models import Type


class TypeCRUD(BaseObjectCRUD):
    """Класс описывающий поведение типов команд."""
    session: AsyncSession
    __id: int | None
    __name: str | None

    def __init__(
            self,  session: AsyncSession, id: int = None, name: str = None
    ):
        self.__session = session
        self.__name = name
        self.__id = id

    async def create(self) -> bool:
        """Создание объекта в базе данных."""
        self.__session.add(Type(name=self.__name))
        await self.__session.commit()
        return True

    async def read(self) -> Type | None:
        """Чтение объекта из базы данных."""
        if self.__id:
            query = (
                select(Type).
                where(Type.id == self.__id)
            )
            return await execute_first_object(self.__session, query)
        elif self.__name:
            query = (
                select(Type).
                where(Type.name == self.__name)
            )
            return await execute_first_object(self.__session, query)

    async def update(self, new_name: str) -> bool:
        """Обновление объекта в базы данных."""
        self.__name = new_name

        obj = await self.read()
        obj.name = self.__name,

        self.__session.add(obj)
        await self.__session.commit()
        return True

    async def delete(self) -> bool:
        """Удаление объекта из базы данных."""
        a = await self.read()
        await self.__session.delete(await self.read())
        await self.__session.commit()
        return True
