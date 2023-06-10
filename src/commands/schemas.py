from pydantic import BaseModel


class CommandScheme(BaseModel):
    id: int
    type: str
    request: str
    response: str


class CommandCreateScheme(BaseModel):
    type: str
    request: str
    response: str
