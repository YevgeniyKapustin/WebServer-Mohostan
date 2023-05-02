from pydantic import BaseModel


class TypeWithoutIDScheme(BaseModel):
    name: str


class TypeScheme(TypeWithoutIDScheme):
    id: int
