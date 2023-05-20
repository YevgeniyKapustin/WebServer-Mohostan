from abc import ABC, abstractmethod


class BaseObjectCRUD(ABC):
    @abstractmethod
    async def create(self) -> bool:
        """Создание объекта в базе данных."""

    @abstractmethod
    async def read(self) -> object:
        """Чтение объекта из базы данных."""

    @abstractmethod
    async def update(self, data_for_update: tuple) -> bool:
        """Обновление объекта в базе данных."""

    @abstractmethod
    async def delete(self) -> bool:
        """Удаление объекта из базы данных."""
