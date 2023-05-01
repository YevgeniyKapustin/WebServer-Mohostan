from pydantic import BaseModel


class OkResponse(BaseModel):
    message: str = "OK"
    description: str = "Выполнено"


class CreateResponse(BaseModel):
    message: str = "Create"
    description: str = "Создано"


class UnpassableEntityResponse(BaseModel):
    message: str = "UnpassableEntity"
    description: str = "Ошибка валидации"
