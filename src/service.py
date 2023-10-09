from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class BaseCRUD(ABC):
    """Абстрактный класс для создания классов, реализующих CRUD логику."""
    @abstractmethod
    async def create(self, session: AsyncSession) -> bool:
        """Создание объекта в базе данных."""

    @abstractmethod
    async def get(self, session: AsyncSession) -> list[object]:
        """Чтение объекта из базы данных."""

    async def get_same(self, session: AsyncSession) -> list[object]:
        """Чтение такого же объекта из базы данных."""
        return await self.get(session)

    @abstractmethod
    async def update(
            self, data_for_update: dict, session: AsyncSession
    ) -> bool:
        """Обновление объекта в базе данных."""

    @abstractmethod
    async def delete(self, session: AsyncSession) -> bool:
        """Удаление объекта из базы данных."""
