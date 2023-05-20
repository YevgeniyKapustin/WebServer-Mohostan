"""Модуль для сбора переменных окружения и переменных конфигурации"""
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# переменные окружения
# FastApi
SECRET_KEY: str = getenv('SECRET_KEY')

# Postgres
POSTGRES_USER: str = getenv('POSTGRES_USER')
POSTGRES_PASSWORD: str = getenv('POSTGRES_PASSWORD')
POSTGRES_HOST: str = getenv('POSTGRES_HOST')
POSTGRES_PORT: str = getenv('POSTGRES_PORT')
POSTGRES_DB: str = getenv('POSTGRES_DB')

# JWT Token
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
JWT_ALGORITHM: str = getenv('JWT_ALGORITHM')

# переменные конфигурации
POSTGRES_URL: str = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
    f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)
TOKEN_URL: str = 'api/v1/auth/login'
