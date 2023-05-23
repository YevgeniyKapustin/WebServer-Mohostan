import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.commands.router import router as command_router
from src.types.router import router as types_router
from src.users.router import router as users_router

app = FastAPI(
    title='Мохостан',
    version='1.0',
)
app.include_router(users_router)
app.include_router(types_router)
app.include_router(command_router)


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url(
        'redis://localhost', encoding='utf8', decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
