from pydantic import BaseModel


class TypeScheme(BaseModel):
    id: int
    name: str


class TypeCreateScheme(BaseModel):
    name: str
