from sqlalchemy import Column, Integer, String

from src.database import Base


class Video(Base):
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(), nullable=False)
    path: str = Column(String(), nullable=False)
