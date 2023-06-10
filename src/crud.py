from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class BaseObjectCRUD(ABC):
    @abstractmethod
    async def create(self, session: AsyncSession) -> bool:
        """Создание объекта в базе данных."""

    @abstractmethod
    async def read(self, session: AsyncSession) -> list[object]:
        """Чтение объекта из базы данных."""

    @abstractmethod
    async def update(
            self, data_for_update: dict, session: AsyncSession
    ) -> bool:
        """Обновление объекта в базе данных."""

    @abstractmethod
    async def delete(self, session: AsyncSession) -> bool:
        """Удаление объекта из базы данных."""
