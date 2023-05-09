"""Модуль для сбора переменных окружения и переменных конфигурации"""
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# переменные окружения
POSTGRES_USER: str = getenv('POSTGRES_USER')
POSTGRES_PASSWORD: str = getenv('POSTGRES_PASSWORD')
POSTGRES_HOST: str = getenv('POSTGRES_HOST')
POSTGRES_PORT: str = getenv('POSTGRES_PORT')
POSTGRES_DB: str = getenv('POSTGRES_DB')
SECRET_KEY: str = getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
ALGORITHM: str = getenv('ALGORITHM')

# переменные конфигурации
POSTGRES_URL: str = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
    f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)
TOKEN_URL = 'api/v1/auth/login'
