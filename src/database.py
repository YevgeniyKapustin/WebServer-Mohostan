"""Сбор метаданных и создание сессии"""
from typing import AsyncGenerator


from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, AsyncEngine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeMeta
from sqlalchemy.pool import NullPool

from src.config import POSTGRES_URL

Base: DeclarativeMeta = declarative_base()

engine: AsyncEngine = create_async_engine(POSTGRES_URL, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
