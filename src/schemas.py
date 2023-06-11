from pydantic import BaseModel


class OkScheme(BaseModel):
    """Схема 200 OK."""
    message: str = 'OK'
    description: str = 'Выполнено'


class CreateScheme(BaseModel):
    """Схема 201 Create."""
    message: str = 'Create'
    description: str = 'Создано'


class BadRequestScheme(BaseModel):
    """Схема 400 BadRequest."""
    message: str = 'BadRequest'
    description: str = 'Ошибочный запрос'


class UnauthorizedScheme(BaseModel):
    """Схема 401 Unauthorized."""
    message: str = 'Unauthorized'
    description: str = 'Вы не авторизованы'


class NotFoundScheme(BaseModel):
    """Схема 404 NotFound."""
    message: str = 'NotFound'
    description: str = 'Объект не найден'


class UnpassableEntityScheme(BaseModel):
    """Схема 422 UnpassableEntity."""
    message: str = 'UnpassableEntity'
    description: str = 'Ошибка валидации'
