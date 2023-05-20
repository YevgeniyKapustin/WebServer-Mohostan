from commands_types.services import TypeCRUD
from src.crud import BaseObjectCRUD
from src.database import session
from src.commands.models import Command
from src.commands_types.models import Type


class CommandCRUD(BaseObjectCRUD):
    """Класс описывающий поведение команд."""
    __id: int | None
    __type: Type | None
    __request: str | None
    __response: str | None

    def __init__(
            self,
            id_: int = None,
            type_: Type = None,
            request: str = None,
            response: str = None
    ):
        self.__id: int = id_
        self.__type: Type = type_
        self.__request: str = request
        self.__response: str = response

    async def create(self) -> bool:
        """Создание объекта в базе данных."""
        session.add(
            Command(
                type_id=self.__type.id,
                request=self.__request,
                response=self.__response,
            )
        )
        session.commit()
        return True

    async def read(self) -> Command | None:
        """Чтение объекта из базы данных."""
        if self.__id:
            return (
                session.query(Command).
                where(Command.id == self.__id).
                first()
            )
        elif self.__request and self.__type and self.__response:
            return (
                session.query(Command).
                where(
                    Command.request == self.__request,
                    Command.type_id == self.__type.id,
                    Command.response == self.__response,
                ).
                first()
            )

    async def update(self, new_obj: dict) -> bool:
        """Обновление объекта в базы данных."""
        self.__request = new_obj.get('request')
        self.__response = new_obj.get('response')
        self.__type = await TypeCRUD(id_=new_obj.get('type_id')).read()

        obj = await self.read()
        obj.type_id = self.__type.id,
        obj.request = self.__request,
        obj.response = self.__response,

        session.add(obj)
        session.commit()
        return True

    async def delete(self) -> bool:
        """Удаление объекта из базы данных."""
        session.delete(await self.read())
        session.commit()
        return True
