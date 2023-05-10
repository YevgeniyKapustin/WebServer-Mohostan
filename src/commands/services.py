from src.database import session
from src.commands.models import Type


class TypeCRUD(object):
    """Класс описывающий возможное поведение типов сообщений."""
    __name: str

    def __init__(self, name: str):
        self.__name = name

    async def create(self) -> bool:
        """Создание объекта в базе данных"""
        session.add(Type(name=self.__name))
        session.commit()
        return True

    async def read(self) -> Type:
        """Чтение объекта из базы данных"""
        a = (
            session.query(Type).
            where(Type.name == self.__name).
            first()
        )
        return a

    async def update(self, new_name: str) -> bool:
        """Обновление объекта в базы данных"""
        self.__name = new_name
        session.add(Type(name=self.__name))
        session.commit()
        return True

    async def delete(self) -> bool:
        """Удаление объекта из базы данных"""
        session.delete(await self.read())
        session.commit()
        return True
