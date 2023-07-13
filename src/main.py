import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from loguru import logger
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.config import settings
from src.commands.router import router as command_router
from src.users.router import router as users_router
from src.videos.router import router as video_router

app = FastAPI(
    title='Мохостан',
    version='1.0',
)
app.include_router(users_router)
app.include_router(command_router)
app.include_router(video_router)

app.mount('/static', StaticFiles(directory='static'), name='uploads')


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ORIGINS],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
    allow_headers=[
        'Access-Control-Allow-Headers', 'Access-Control-Allow-Origin',
        'Content-Type', 'Set-Cookie', 'Authorization'
    ],
)


logger.add('log.txt', format='{time} {level} {message}')


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url(
        'redis://localhost', encoding='utf8', decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
