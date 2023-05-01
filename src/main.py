import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.commands_types.router import router as types_router

app = FastAPI(
    title='Ванесса',
    version='1.0',
    description='API созданное для ванессы, впрочем, оно доступно всем',
    openapi_tags=[
        {
            'name': 'Типы команд',
            'description': 'Поле "type" для команд',
        }
    ],
)
app.include_router(types_router)


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url(
        'redis://localhost', encoding='utf8', decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
