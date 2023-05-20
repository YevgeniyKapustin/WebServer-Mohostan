from pydantic import BaseModel


class CommandScheme(BaseModel):
    id: int
    type_id: int
    request: str
    response: str


class CommandCreateScheme(BaseModel):
    type_id: int
    request: str
    response: str
