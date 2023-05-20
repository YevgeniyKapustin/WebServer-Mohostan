from src.crud import BaseObjectCRUD
from src.database import session
from src.commands_types.models import Type


class TypeCRUD(BaseObjectCRUD):
    """Класс описывающий поведение типов команд."""
    __id: int | None
    __name: str | None

    def __init__(self,  id_: int = None, name: str = None):
        self.__name = name
        self.__id = id_

    async def create(self) -> bool:
        """Создание объекта в базе данных."""
        session.add(Type(name=self.__name))
        session.commit()
        return True

    async def read(self) -> Type | None:
        """Чтение объекта из базы данных."""
        if self.__id:
            return (
                session.query(Type).
                where(Type.id == self.__id).
                first()
            )
        elif self.__name:
            return (
                session.query(Type).
                where(Type.name == self.__name).
                first()
            )

    async def update(self, new_name: str) -> bool:
        """Обновление объекта в базы данных."""
        self.__name = new_name

        obj = await self.read()
        obj.name = self.__name,

        session.add(obj)
        session.commit()
        return True

    async def delete(self) -> bool:
        """Удаление объекта из базы данных."""
        session.delete(await self.read())
        session.commit()
        return True
