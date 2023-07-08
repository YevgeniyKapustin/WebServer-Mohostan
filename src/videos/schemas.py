from fastapi import UploadFile
from pydantic import BaseModel


class AddVideoScheme(BaseModel):
    title: str
    file: UploadFile


class VideoScheme(BaseModel):
    id: int
    title: str
    path: str | None


class VideoCreateScheme(BaseModel):
    title: str | None
