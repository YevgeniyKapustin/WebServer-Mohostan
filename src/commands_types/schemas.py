from pydantic import BaseModel


class TypeScheme(BaseModel):
    id: int
    name: str


class NewTypeScheme(BaseModel):
    current_name: str
    new_name: str
