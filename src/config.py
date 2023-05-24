"""Модуль для сбора переменных окружения и переменных конфигурации"""
from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__()
        self.POSTGRES_URL: str = self.__get_postgres_dsn('async_fallback=True')
        self.TEST_POSTGRES_URL: str = self.__get_postgres_dsn()

    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_URL: str = None

    # Test Postgres
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_PORT: str
    TEST_POSTGRES_DB: str
    TEST_POSTGRES_URL: str = None

    # JWT Token
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str
    TOKEN_URL: str = 'api/v1/auth/login'

    def __get_postgres_dsn(self, query: str | None = None) -> str:
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=f'/{self.POSTGRES_DB}',
            query=query
        )

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'
