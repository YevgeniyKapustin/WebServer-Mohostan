import asyncio
import json
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker
)
from sqlalchemy.pool import NullPool

from src.config import TEST_POSTGRES_URL
from src.database import get_async_session, Base
from src.main import app
from src.users.models import User

test_engin: AsyncEngine = create_async_engine(
    TEST_POSTGRES_URL, poolclass=NullPool
)
async_session_maker = async_sessionmaker(test_engin, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with test_engin.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await create_trust_user()
    yield
    async with test_engin.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_session() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_session:
        yield async_session


async def user_token():
    async with async_session_maker() as session:
        response = session.post(
            'api/v1/auth/login',
            data={
                'username': 'dev@test.com',
                'password': '666',
            }
        )
        decode_response: str = response.content.decode('UTF-8')
        data: dict = json.loads(decode_response)
        return data.get('access_token')


async def create_trust_user():
    async with async_session_maker() as session:
        obj = User(
            email='dev@test.com',
            hashed_password=(  # 666
                '$2b$12$EBg3fGaSyuPFoph4AAbeAeENjI9zj19KFwsbVrAGKYKbyPWrM8Qyi'
            ),
            is_trusted=True
        )
        session.add(obj)
        await session.commit()
