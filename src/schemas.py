"""Стандартные схемы для HTTP ответов."""
from pydantic import BaseModel


class OkScheme(BaseModel):
    """Схема 200 OK."""
    message: str = 'OK'
    description: str = 'Выполнено'


class CreateScheme(BaseModel):
    """Схема 201 Create."""
    message: str = 'Create'
    description: str = 'Создано'


class NoContentScheme(BaseModel):
    """Схема 204 NoContent."""
    message: str = 'NoContent'
    description: str = 'Объект остался прежним'


class NotFoundScheme(BaseModel):
    """Схема 404 NotFound."""
    message: str = 'NotFound'
    description: str = 'Объект не найден'


class UnpassableEntityScheme(BaseModel):
    """Схема 422 UnpassableEntity."""
    message: str = 'UnpassableEntity'
    description: str = 'Ошибка валидации'
