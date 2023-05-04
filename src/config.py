"""Модуль для сбора переменных окружения"""
from dotenv import load_dotenv
from os import environ

load_dotenv()

POSTGRES_USER: str = environ.get('POSTGRES_USER')
POSTGRES_PASSWORD: str = environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST: str = environ.get('POSTGRES_HOST')
POSTGRES_PORT: str = environ.get('POSTGRES_PORT')
POSTGRES_DB: str = environ.get('POSTGRES_DB')
POSTGRES_URL: str = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
    f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
)
