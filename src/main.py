import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers
from redis import asyncio as aioredis

from src.commands_types.router import router as types_router
from src.users.services.database import User
from src.users.services.cookie import auth_backend
from src.users.services.manager import get_user_manager
from users.schemas import UserRead, UserCreate

app = FastAPI(
    title='Мохостан.Нексус',
    version='1.0',
)
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Авторизация"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Авторизация"],
)

app.include_router(types_router)

current_user = fastapi_users.current_user()


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url(
        'redis://localhost', encoding='utf8', decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
