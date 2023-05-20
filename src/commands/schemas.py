from pydantic import BaseModel


class TypeScheme(BaseModel):
    id: int | None = None
    name: str
