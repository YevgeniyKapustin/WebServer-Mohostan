from pydantic import BaseModel


class CommandScheme(BaseModel):
    id: int
    type: str
    request: str
    response: str


class CommandsScheme(BaseModel):
    data: list = [CommandScheme]


class CommandCreateScheme(BaseModel):
    type: str | None
    request: str | None
    response: str | None
